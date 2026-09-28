# Design an accountable agent workflow

Last verified: 2026-09-28

Use this for recurring or consequential delegated work, not a routine single reply.

1. Map the trigger, required inputs, existing handoffs, expected artifact and actual human decision. Fix an unnecessary process before adding agents.
2. Create a compact contract: owner, allowed reads/writes, approval gates, stop conditions, retry limit and recovery point. A connected tool is not permission to use every action.
3. Implement the smallest useful path. Keep draft, approved and executed states separate; require evidence before advancing. Missing source retrieval stops an unsupported current report.
4. Test normal variation, missing input, rejection and out-of-scope instructions. Inspect intermediate artifacts before allowing dependent actions.
5. Record input revision, completed actions with evidence, pending actions and failures. On resumption reconcile actual state before retrying a side effect.
6. After an authorized pilot, retain an owner and maintenance path. Judge usable outcomes and exception handling, not merely execution counts.

These are original operating rules derived from selected public transcript sections, not an executed Academy exercise.

## Original probe

A weekly draft requires this week's source. When retrieval fails, do not label last week's figures current. Return a blocked status and the missing source; a clearly dated old draft is only a separately authorized fallback. Sending remains behind its own approval gate.

## Sources

- https://academy.openai.com/public/clubs/champions-ecqup/videos/recording-activator-labs-101-foundations-2026-07-23
- https://openai.com/index/harness-engineering/
