---
description: 'Generated from evals/questions.json case scope-04'
tags: [routing, should-not-trigger]
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

Refactor this to async/await: function load(cb){ setTimeout(() => cb(42), 10) }
