# ChatGPT Project Instructions — Claude Stack Router

Claude / Anthropic に関するタスクでは、一般的で安定した知識だけで十分なら外部参照しない。

Claude固有の仕様、Claude Code、Agent Skills、MCP、API、モデル選択、prompting、Claudeと他AIの連携など、変更されやすい仕様または重要な設計判断が関わる場合は、GitHub の `atsushi-matsuoka/claude-knowledge` にある `ecosystem-guide` を必要な範囲だけ参照する。

まず `skills/ecosystem-guide/SKILL.md` を確認し、タスクに直接必要な reference だけ読む。保存情報が古い可能性がある場合は Anthropic の最新公式一次資料で再確認する。

Claude と無関係なタスクではこのリポジトリを参照しない。
