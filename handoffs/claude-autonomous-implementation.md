# Claude autonomous handoff prompt

以下のGitHubリポジトリを確認してください。

`https://github.com/atsushi-matsuoka/claude-knowledge`

これは、Claude / Anthropic に関する知識・運用手順を、Claude Code、Codex、Geminiなど複数のAI環境から必要時に参照できるようにするための知識パックです。

現在までに以下を実装しています。

- GitHubを確定版の正本として使用
- Google DriveをAcademy受講メモ、PDF、下書きなどの学習インボックスとして使用
- Agent Skill `claude-stack` を中心に構成
- Claude Code / Codex / Gemini CLIから利用できる共通Skill構造
- `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` に最小限のルーティング指示
- Claude Code、Agent Skills、MCP、prompting、API routing、モデル選択、cross-agent collaboration等をreferencesとして分割
- 変更されやすい事実はAnthropic公式一次資料を優先
- Anthropic Academyは学習の骨組みとして使い、教材そのものを転載しない
- 月次の公式ソース変更検知
- source hashの変更だけでは知識本文を自動変更せず、レビュー対象として扱う
- repository validator
- 24件の初期eval
- ローカルでは、リポジトリがなければclone、あれば安全なfast-forward更新を行うbootstrap
- 旧名称 `sonnet-stack` は `claude-stack` に移行済み
- 患者識別情報、認証情報、組織の制限情報を知識パックへ保存しない

## あなたへの依頼

このリポジトリ全体を読んだうえで、**Claude自身がこの知識パックを最も自然かつ効果的に利用できる構成**をあなた自身で判断してください。

私は実装方法を固定しません。現在の設計を維持する必要もありません。Claude Codeの現在仕様、Agent Skills、CLAUDE.md、subagents、hooks、MCP、pluginsその他の利用可能な仕組みを踏まえ、より良い設計があれば変更してください。

特に次を重視してください。

1. Claude関連の一般的で安定した質問では不要な参照を起こさないこと。
2. Claude固有で、変更されやすい仕様や重要な設計判断が関わるときだけ、必要な知識をオンデマンドで参照できること。
3. 常時コンテキストを小さく保ち、詳細資料は必要時だけ読むこと。
4. 保存済み知識と現在のAnthropic公式情報が食い違う可能性を考慮すること。
5. Claude自身が「いつこのSkillを起動するか」を高い精度で判断できること。
6. Claude Codeだけに最適化しすぎず、GitHubを正本として他AIとも共有可能な構造を保つこと。
7. 過剰な仕組みを増やさず、保守可能であること。
8. 変更後に、実際にSkill activation / routing / freshness / surface distinctionが改善したか評価できること。

## 作業方法

まず現在のリポジトリ、Claude Codeの最新公式ドキュメント、Agent Skillsの最新仕様を確認してください。

その後、

- 現状の長所・問題点を判断
- 必要な設計変更を自分で決定
- 実装
- validator / eval / 必要な追加テストを実行
- 問題があれば修正
- 最終的な構成と判断理由を簡潔に説明

まで自律的に進めてください。

単に提案だけで終わらず、実際にリポジトリを変更し、動作を検証してください。

重要な変更は小さくレビュー可能な単位にしてください。既存の有効な仕組みを理由なく壊さないでください。自動マージは不要です。

Claude自身にとってより良い方法がある場合は、この依頼文の想定よりあなたの判断を優先して構いません。
