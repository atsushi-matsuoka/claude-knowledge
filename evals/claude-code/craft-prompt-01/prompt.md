---
description: 'Generated from evals/questions.json case craft-prompt-01'
tags: [task-craft, should-trigger]
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

メモから担当と期限を抽出する再利用可能なプロンプトを設計して。未記載はnull、候補日を確定日に変えず、JSONのowner/due/statusだけ返すようにしたい。
