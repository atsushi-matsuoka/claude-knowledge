#!/usr/bin/env python3
"""One-time, guarded migration on feat/task-craft-v0.3.0; removed before validation."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT/path).read_text(encoding='utf-8')

def write(path, text):
    p = ROOT/path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def replace_once(text, before, after):
    if text.count(before) != 1:
        raise RuntimeError('Unexpected baseline for anchor: ' + repr(before[:120]))
    return text.replace(before, after, 1)

# Preserve ecosystem-guide behavior; version is the only SKILL.md edit.
plugin = json.loads(read('.claude-plugin/plugin.json'))
assert plugin['version'] == '0.2.0'
plugin['version'] = '0.3.0'
plugin['description'] = 'Two focused skills: ecosystem-guide for Claude product routing and freshness; task-craft for prompt design, testable specifications and bounded AI workflows.'
write('.claude-plugin/plugin.json', json.dumps(plugin, indent=2, ensure_ascii=False)+'\n')
write('skills/ecosystem-guide/SKILL.md', replace_once(read('skills/ecosystem-guide/SKILL.md'), 'version: 0.2.0', 'version: 0.3.0'))
write('CHANGELOG.md', replace_once(read('CHANGELOG.md'), '# Changelog\n', '''# Changelog

## 0.3.0 - 2026-09-27

- Added `task-craft`: practical prompt/spec/workflow design, failure diagnosis, original examples and outcome evaluation, separate from product knowledge.
- Recorded exactly which public educational text and official docs were reviewed; Academy lesson completion and real-model effectiveness remain unclaimed.
- Added 24 task-craft routing/artifact cases and nine synthetic downstream fixtures with a strict offline scorer.
- Generalized validation, generated evals and bootstrap to multiple skills while preserving the existing ecosystem-guide cases and description.
- Registered the new method sources for monthly monitoring and refreshed fetch baselines.
- Existing historical handoffs and v0.2.0 measurement records remain unchanged below their new status notes. No automatic merge or paid evaluation.
'''))

# Split single-skill validation into a reusable per-skill helper.
v = read('scripts/validate_repository.py')
start = v.index('    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")')
end = v.index('    # --- Plugin / marketplace', start)
block = v[start:end]
block = block.replace('return errors, warnings', 'return errors, warnings, {}')
anchor = '            text = f.read_text(encoding="utf-8")\n'
block = replace_once(block, anchor, anchor + '''            if sub == "references" and not re.search(r"^## Sources\\s*$", text, re.M):
                message = f"{rel} missing '## Sources'"
                if skill_dir.name == "ecosystem-guide":
                    warnings.append(message + " (pre-existing reference; review separately)")
                else:
                    errors.append(message)
''')
helper = '''def validate_skill(skill_dir: Path, today: date):
    """Apply the same portable-skill and context-budget checks to every skill."""
    errors: list[str] = []
    warnings: list[str] = []
''' + block + '    return errors, warnings, fm\n\n\n'
section_start = v.index('    # --- Skill ')
v = v[:section_start] + '''    # --- Skills --------------------------------------------------------------
    skill_dirs = sorted(d for d in (root / "skills").glob("*") if (d / "SKILL.md").exists())
    if not skill_dirs:
        errors.append("Expected at least one skill under skills/")
        return errors, warnings
    skill_metadata = {}
    for skill_dir in skill_dirs:
        skill_errors, skill_warnings, skill_fm = validate_skill(skill_dir, today)
        errors.extend(f"{skill_dir.name}: {e}" for e in skill_errors)
        warnings.extend(f"{skill_dir.name}: {w}" for w in skill_warnings)
        skill_metadata[skill_dir.name] = skill_fm

''' + v[end:]
v = replace_once(v, 'def validate(root:', helper+'def validate(root:')
old = '''    meta_version = re.search(r"^\\s+version:\\s*(\\S+)", fm.get("metadata", ""), re.M)
    if not meta_version or meta_version.group(1) != version:
        errors.append("SKILL.md metadata.version must equal plugin.json version")
'''
new = '''    for skill_name, skill_fm in skill_metadata.items():
        meta_version = re.search(r"^\\s+version:\\s*(\\S+)", skill_fm.get("metadata", ""), re.M)
        if not meta_version or meta_version.group(1) != version:
            errors.append(f"{skill_name}: SKILL.md metadata.version must equal plugin.json version")
'''
v = replace_once(v, old, new)
v = replace_once(v,
    '    ref_stems = {f.stem for sub in ("references", "workflows") for f in (skill_dir / sub).glob("*.md")}\n',
    '    ref_stems = {d.name: {f.stem for sub in ("references", "workflows") for f in (d / sub).glob("*.md")} for d in skill_dirs}\n')
v = replace_once(v,
    '        if c.get("reads") and c["reads"] not in ref_stems:\n',
    '''        target = c.get("skill", "ecosystem-guide")
        if target not in ref_stems:
            errors.append(f"Eval {c.get('id')} targets unknown skill '{target}'")
        if c.get("reads") and c["reads"] not in ref_stems.get(target, set()):
''')
v = replace_once(v, '    build = root / "scripts/build_evals.py"\n', '''    if evals.get("schema_version") != 2:
        errors.append("evals/questions.json must use schema_version 2")
    for target in ref_stems:
        own = [c for c in cases if c.get("skill", "ecosystem-guide") == target]
        if len(own) < MIN_CASES:
            errors.append(f"{target}: need at least {MIN_CASES} eval cases")
        if sum(c.get("should_trigger") is False for c in own) < MIN_NEGATIVE_CASES:
            errors.append(f"{target}: need at least {MIN_NEGATIVE_CASES} should-not-trigger cases")
    build = root / "scripts/build_evals.py"
''')
write('scripts/validate_repository.py', v)

# Preserve old generated cases byte-for-byte; explicit `skill` selects new targets.
b = read('scripts/build_evals.py')
b = replace_once(b, '    if len(names) != 1:\n', '    if "ecosystem-guide" in names:\n        return "ecosystem-guide"\n    if len(names) != 1:\n')
b = replace_once(b, 'render_case(case, skill).items()', 'render_case(case, case.get("skill", skill)).items()')
b = replace_once(b, '        read_pattern = js_escape(case["reads"]) + r"\\.md"\n', '''        read_pattern = js_escape(case["reads"]) + r"\\.md"
        if case.get("skill"):
            read_pattern = js_escape(skill + "/") + r"(?:references|workflows)\\/" + read_pattern
''')
write('scripts/build_evals.py', b)
q = json.loads(read('evals/questions.json'))
old_cases = json.loads(json.dumps(q['cases']))
added = json.loads(read('.bootstrap/task-craft-cases.json'))
assert len(added) == 24 and not {c['id'] for c in added} & {c['id'] for c in old_cases}
for c in added:
    c['skill'] = 'task-craft'
    c['tags'] = ['task-craft'] + c.get('tags', [])
q['cases'].extend(added)
assert q['cases'][:len(old_cases)] == old_cases
q['notes'] += ' Optional skill selects the graded skill; omitted means ecosystem-guide. task-craft cases measure practice artifacts separately. See TASK_CRAFT.md for downstream outcome tests.'
write('evals/questions.json', json.dumps(q, indent=2, ensure_ascii=False)+'\n')

# Link both skills for Codex/Gemini; Claude still explicitly opts into local links.
b = read('scripts/bootstrap.py')
b = replace_once(b, 'SKILL_NAME = "ecosystem-guide"\n', 'SKILL_NAME = "ecosystem-guide"  # Backward-compatible primary name.\nSKILL_NAMES = ("ecosystem-guide", "task-craft")\n')
b = replace_once(b, '''    skill = dest/"skills"/SKILL_NAME
    if not (skill/"SKILL.md").exists():
        raise RuntimeError(f"Skill not found: {skill}")

    # Codex USER scope. Gemini CLI also supports ~/.agents/skills as an alias.
    install_link(skill, Path.home()/".agents"/"skills"/SKILL_NAME)
    if ns.claude_code:
        install_link(skill, Path.home()/".claude"/"skills"/SKILL_NAME)
''', '''    skills = [(name, dest/"skills"/name) for name in SKILL_NAMES]
    for name, skill in skills:
        if not (skill/"SKILL.md").exists():
            raise RuntimeError(f"Skill not found: {skill}")

    # Validate all sources before changing any installation links.
    for name, skill in skills:
        install_link(skill, Path.home()/".agents"/"skills"/name)
        if ns.claude_code:
            install_link(skill, Path.home()/".claude"/"skills"/name)
''')
write('scripts/bootstrap.py', b)
t = read('tests/test_pack.py')
t = replace_once(t, 'self.skill = next((self.repo / "skills").glob("*/SKILL.md"))', 'self.skill = self.repo / "skills" / "ecosystem-guide" / "SKILL.md"')
t = replace_once(t, 'today=date(2026, 9, 26)', 'today=date.today()')
t = replace_once(t, 'self.assertIn("ecosystem-guide", grader)', 'self.assertIn(c.get("skill", "ecosystem-guide"), grader)')
write('tests/test_pack.py', t)

# Add watched primary sources. The workflow will refresh actual network baselines.
m = json.loads(read('sources/manifest.json'))
new_sources = [
 ('anthropic-prompt-overview', 'https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview', '.md', 'Success criteria before prompt optimization'),
 ('anthropic-prompt-practices', 'https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices', '.md', 'Current prompting methods; do not freeze model-specific folklore'),
 ('anthropic-develop-tests', 'https://platform.claude.com/docs/en/test-and-evaluate/develop-tests', '.md', 'Task-representative success criteria and evaluators'),
 ('anthropic-effective-agents', 'https://www.anthropic.com/engineering/building-effective-agents', '', 'Proportionate workflows and bounded autonomy'),
 ('anthropic-context-engineering', 'https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents', '', 'Selective context and durable handoffs'),
 ('anthropic-agent-evaluation', 'https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents', '', 'Trace versus outcome and evaluation hygiene'),
 ('anthropic-course-prompt-process', 'https://github.com/anthropics/courses/blob/master/real_world_prompting/03_prompt_engineering.ipynb', 'https://raw.githubusercontent.com/anthropics/courses/master/real_world_prompting/03_prompt_engineering.ipynb', 'Public educational text on diagnose/change/retest; not Academy course completion')
]
for sid, url, fetch_suffix, purpose in new_sources:
    assert sid not in {s['id'] for s in m['sources']}
    fetch_url = fetch_suffix if fetch_suffix.startswith('https://') else url+fetch_suffix
    m['sources'].append({'id':sid, 'vendor':'anthropic', 'url':url, 'fetch_url':fetch_url, 'purpose':purpose, 'volatility':'medium', 'review_days':30})
m['last_curated'] = '2026-09-27'
write('sources/manifest.json', json.dumps(m, indent=2, ensure_ascii=False)+'\n')

# Shared instructions, maintenance and human-facing entry points.
a = read('AGENTS.md')
a = replace_once(a,
 '- The shared Agent Skill is `skills/ecosystem-guide/`. Follow its `workflows/update-knowledge-pack.md` when changing knowledge.',
 '- Two focused skills share this pack: `skills/ecosystem-guide/` for product facts/routing, and `skills/task-craft/` for applying prompting, specification and evaluation methods. Follow ecosystem-guide\'s `workflows/update-knowledge-pack.md` when maintaining either.')
a += '\n- Preserve skill boundaries: simple direct tasks should not become prompt-design projects. Do not load product documentation for stable method application alone.\n- Keep the existing ecosystem-guide cases and holdouts unchanged when extending task-craft. New cases select `skill` explicitly; generated suites remain generated.\n- Distinguish Academy outlines, read lesson text, exercised notebooks and measured outcomes. Use `academy-notes/2026-09-27-practice-intake.md` and `evals/TASK_CRAFT.md`; do not claim Academy completion or model-quality gains without evidence.\n'
write('AGENTS.md', a)
w = read('skills/ecosystem-guide/workflows/update-knowledge-pack.md')
w += '''
## Practice-layer additions

- For task-craft, start from an actual failure or a retrieved educational section. Record source coverage and whether it was only an outline, read text, exercised material or a measured behavior.
- Convert a learned principle into an original procedure, example and acceptance check. Do not add prose merely to enlarge the knowledge base.
- Put dated practical guidance in task-craft references. Stable method application does not require a live fetch on every user task; version-specific product claims still do.
- New task-craft cases in questions.json use `skill: task-craft`. Preserve the existing ecosystem-guide cases and untouched holdouts. Rebuild generated cases.
- Separate activation/artifact grading from downstream task results. Follow evals/TASK_CRAFT.md; without a real model run report effect unmeasured. Never run paid evaluation automatically.
- Keep every skill metadata.version, plugin.json version and top CHANGELOG entry aligned. New fetch_url entries require an actual baseline refresh; keep failed retrievals visible.
- Do not edit historical handoffs, auto-merge, or claim a PR is installed on the user's accounts.
'''
write('skills/ecosystem-guide/workflows/update-knowledge-pack.md', w)
r = read('README.md')
r = r.replace('A reviewed, version-controlled knowledge pack', 'A reviewed, version-controlled knowledge and practice pack', 1)
r = replace_once(r, '- **One portable skill, `ecosystem-guide`.** Written to the open Agent Skills spec (portable frontmatter only, no reserved words in the name), so the same folder works as a Claude plugin skill, a claude.ai upload, and a Codex/Gemini skill.', '- **Two focused portable skills.** `ecosystem-guide` handles changing Claude product knowledge; `task-craft` applies prompting, specification and evaluation methods. Each uses portable frontmatter and can be distributed in this plugin or installed separately.')
lines = r.splitlines()
for i, line in enumerate(lines):
    if line.startswith('- **Small always-on footprint.'):
        lines[i] = '- **Small always-on footprint.** Hosts see concise descriptions; each skill body and its matching references load only when needed. Do not load both entire folders for every request.'
    elif line.startswith('- **Trigger narrowly.'):
        lines[i] = '- **Different triggers.** Product/surface questions use ecosystem-guide. Prompt design, substantial idea-to-spec work and AI workflow improvement use task-craft. Simple direct execution and stable conceptual explanations need neither practice procedure nor extra retrieval.'
    elif line.startswith('- **Measured, not assumed.'):
        lines[i] = '- **Measured, not assumed.** Historical ecosystem-guide results remain in evals/RESULTS.md. task-craft has test infrastructure but its model effectiveness is unmeasured; activation, artifact quality and downstream outcomes are separate.'
r = '\n'.join(lines)+'\n'
r = replace_once(r, 'and links `~/.agents/skills/ecosystem-guide`.', 'and links both `~/.agents/skills/ecosystem-guide` and `~/.agents/skills/task-craft`.')
r = replace_once(r, '  agents/openai.yaml   Codex display metadata\n', '  agents/openai.yaml   Codex display metadata\nskills/task-craft/\n  SKILL.md             task-design trigger and work contract\n  references/          original method notes and worked examples\n  workflows/           prompt repair, idea-to-spec, agent planning, iteration\n')
r = replace_once(r, '## Updating knowledge\n', '''## Practice layer: use task-craft for the work itself

For example: 「この曖昧なアイデアを、試せる最小仕様にして」, 「このプロンプトが不確実性を消してしまうので直して」, or 「このAI作業を公平に比較する評価を設計して」. The skill should return a usable artifact, not merely describe Claude features. When a task also depends on current Claude product facts, consult ecosystem-guide only for that subtask.

This first practice layer uses reviewed public Anthropic educational text and official documentation. It does **not** mean the full Academy was learned. Academy pages/lesson bodies not obtained remain incomplete; no exercises or real-model effectiveness tests were executed here. See `academy-notes/2026-09-27-practice-intake.md`, `skills/task-craft/references/learning-provenance.md` and `evals/TASK_CRAFT.md`.

The plugin package now contains both skills. An unmerged PR is not a deployed update: update the installed package only after review and merge. The routing text in `adapters/` is a template, not a claim that account-level instructions were changed.

## Updating knowledge
''')
r = replace_once(r, '## Evaluating routing\n', '''## Evaluating routing

Cases retain schema v2; optional `skill` chooses the graded target, with ecosystem-guide as the backward-compatible default. All new cases carry a task-craft tag. Use `scripts/summarize_evals.py ... --tag task-craft` for that skill and `--exclude-tag task-craft` for the original skill. Do not pool their scores as evidence of improved prompt design. See `evals/TASK_CRAFT.md` for a separate downstream-output comparison.
''')
write('README.md', r)
cm = read('curriculum/academy-map.md')
cm = replace_once(cm, 'Status: scaffolded; fill this in while studying Academy.', 'Status: Academy curriculum remains incomplete. A partial public-method intake was added on 2026-09-27; course completion is not implied.')
cm += '''
## Partial practice intake (2026-09-27)

The table above records Academy course status and is not advanced by reading other documentation. Public Real world prompting lesson 3 text plus selected official method documents now support `skills/task-craft/`. They cover task framing, diagnostic prompt revision, context/handoffs, proportionate workflows and evaluation design. These are applied procedures with original examples, not full Academy course summaries.

Evidence and section coverage: `academy-notes/2026-09-27-practice-intake.md`.
Delivery map: task framing → idea-to-spec; prompting → design-or-repair-prompt; agent/context methods → plan-agent-work; evaluations → test-and-iterate and evals/TASK_CRAFT.md.

Read text: partial. Exercises executed: none. Real-model effectiveness measured: no. Outstanding Academy lessons and user notes should be integrated incrementally rather than marked completed in bulk.
'''
write('curriculum/academy-map.md', cm)
write('evals/RESULTS.md', replace_once(read('evals/RESULTS.md'), '# Eval results\n', '''# Eval results

## 2026-09-27: task-craft / v0.3.0 candidate

Model effectiveness is **unmeasured**. Added activation/artifact cases and a separate downstream-output protocol with an offline scorer; no Claude/Codex/Gemini model run or paid API evaluation was performed for this addition. Tooling/unit-test checks are reported separately in the PR. Do not attribute the historical scores below to task-craft. See evals/TASK_CRAFT.md.
'''))
router = '''単純な翻訳・短い推敲・通常の実装は、その依頼を直接処理する。
AI向けのプロンプト作成・添削、曖昧な大きな依頼の具体化、AI作業の分担・評価改善が必要なときだけ、GitHubの atsushi-matsuoka/claude-knowledge の skills/task-craft/SKILL.md と必要な資料を参照し、実用的な成果物を作る。安定した手法の適用だけで毎回外部検索はしない。
Claude固有の変更されやすい仕様や重要な製品上の設計判断は、skills/ecosystem-guide/SKILL.md と必要な資料を参照し、変わり得る事実はAnthropic公式一次資料で確認する。
両Skillを毎回読み込まず、未取得の資料や未実行の検証を完了扱いしない。アクセスできなければ、その制約を明記する。
'''
write('adapters/chatgpt-project-instructions.md', '# ChatGPT Project instructions — selective routing\n\n'+router)
write('adapters/gemini-routing-instructions.md', '# Gemini instructions — selective routing\n\n'+router+'\nローカルでSkillを利用できる環境では同じ条件でインストール済みSkillを使う。アカウントが同じだけでファイルやGitHubへのアクセスが可能とは仮定しない。\n')

# Temporary inputs must not ship with the reviewed package.
(ROOT/'.bootstrap/task-craft-cases.json').unlink()
Path(__file__).unlink()
print('Prepared task-craft 0.3.0; old cases preserved:', len(old_cases), '; new cases:', len(added))
