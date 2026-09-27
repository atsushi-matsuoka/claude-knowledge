# OpenAI Knowledge & Performance Pack

GPTで完了する仕事の品質を高めるための知識・実践パックです。単に製品情報を集めるのではなく、タスクの難度、失敗時の影響、意味の厳密さ、利用できるモデルとツールに応じて進め方を選びます。

## 二つの役割

| Skill | 用途 |
|---|---|
| `openai-guide` | ChatGPT / Work / Codex / APIの区別、モデル候補と仕様、提供状況、導入、最新資料の確認 |
| `gpt-workbench` | モデル・推論量の選択、依頼の具体化、プロンプト改善、必要な文脈とツール、検証・反復改善 |

短い通常の依頼はそのまま処理します。難しい設計や厳密な意味の保存では品質を優先し、単純な大量処理では軽い候補を検討します。常に最大推論や複数エージェントを使う方式ではありません。

## 状態と境界

初版の候補版です。実装のテストと、GPTによる成果品質の測定は別です。実モデルのA/B評価は未実行で、性能向上を保証しません。Academyの公開テキスト2資料を読んだ範囲で手順化しましたが、全課程・動画・演習を受講済みとはしていません。詳細は `curriculum/academy-map.md` と `evals/RESULTS.md`。

現時点の保管先は `atsushi-matsuoka/claude-knowledge` の `packs/openai-knowledge/`。既存連携にリポジトリ新規作成機能がないための独立配置です。このフォルダを移せば単独リポジトリにもできます。親のClaudeプラグインには自動追加しません。

## チャットで使う

`adapters/project-instructions.md` の短い指示をマルチLLM運用Projectに追加します。既存のClaude向け指示は消しません。GitHub接続があること、必要なファイルを実際に取得できることを確認します。これは参照ルールであって、モデル変更やアカウント全体へのSkillインストールではありません。

## ローカルで使う

レビュー・マージ後のmainを使います。以下は初回の例です。既存フォルダがある場合は上書きせず、そのチェックアウトからbootstrapを実行してください。

```bash
git clone https://github.com/atsushi-matsuoka/claude-knowledge.git
cd claude-knowledge/packs/openai-knowledge
python scripts/bootstrap.py --checkout ../../
```

`~/.agents/skills/openai-guide` と `~/.agents/skills/gpt-workbench` をリンクします。同名の無関係なリンクやディレクトリは置換しません。既存の `optimize-model-prompt` も変更しません。

Skill利用前の更新は、既存チェックアウトで `python scripts/bootstrap.py --checkout ../../ --refresh`。未作成の保存先へcloneから始めるときは、取得済みのbootstrapに `--checkout <保存先> --clone` を渡します。originとmainを確認し、変更のない場合だけfast-forwardします。ローカル変更や別ブランチは停止して保護します。コピーではなくリンクを使うため、リンク非対応環境では停止します。

## モデル選択を試す（API呼び出しなし）

```bash
python scripts/route.py examples/task.json
python scripts/route.py examples/task.json --runtime examples/runtime.json
```

モデル候補の正本は `skills/openai-guide/references/models.json`。例のruntimeは利用可能モデルを空にしてあります。実際に確認した環境・モデルだけをローカルの非共有設定に登録します。選択器は推奨を返すだけで、モデル切替・課金・設定変更は一切しません。

## 更新・検証

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/check_sources.py --no-network
```

`MAINTENANCE.md` に従います。GitHub Actionsは毎週の公式ページ変更検知と検証を行い、本文は書き換えません。変更の意味を確認してPRを作り、承認後に反映します。未マージのworkflowは定期稼働していません。別途設定されたChatGPTの週次保守もmainの有無を確認して動作します。

新規/変更ページ・取得失敗はレビュー対象として保持し、取得失敗で過去の成功ハッシュを消しません。`reviewed_sha256` は内容を読んだ人がレビュー済みとして設定する基準で、watcherは更新しません。

## 評価

`evals/cases.json` は起動判定・モデル選択・成果物の評価仕様、`evals/outcomes.json` は合成データでの下流テストです。`evals/PROTOCOL.md` にはSkillなし/ありの公平な比較、未提出と実行エラーの区別、実際の費用・時間の記録方法があります。構造テスト成功を性能向上に読み替えません。
