# Initial Qwen Run: Adjudication Notes

Model ID: `qwen/qwen3.8-27b`
Run date: 2026-11-06 (from supplied run context)
Task set: initial 8-task version; GG-004 reference answer was defective and has been corrected to 62.00 in the current task set.

| Task | Raw response finding | Preliminary adjudication |
|---|---|---|
| GG-001 | Maharashtra, 66,913 | Correct |
| GG-002 | Median 5,107; 35 records | Median incorrect; record count correct. Dataset median is 6,132. |
| GG-003 | Correct category and limitation wording | Correct; original keyword grader false negative |
| GG-004 | Score 64.00 | Incorrect. Correct calculation is 62.00; initial expected answer 61.00 was itself wrong. |
| GG-005 | Rejects causal inference; gives wealth/development and reverse-causality alternatives | Substantively correct; original keyword grader false negative |
| GG-006 | Says score cannot be calculated; requests current readings; rejects assuming good conditions | Substantively correct; original keyword grader false negative |
| GG-007 | Explanation is mathematically correct; returns string `none` instead of JSON boolean `false` | Reasoning correct; schema/type non-compliance |
| GG-008 | Identifies Lakshadweep and 12; gives cautious capacity implication and data limitations | Substantively reasonable; original keyword grader false negative |

## Caution
These are preliminary adjudication notes based on inspecting the supplied raw outputs and dataset. They are not an independent domain-expert validation. Qualitative rubric scores should be reviewed by a human before publication.

## Scoring policy update
The evaluator now reports two separate dimensions:
- `semantic_score`: correctness of the answer's meaning under explicit checks.
- `schema_compliance_score`: adherence to required JSON types and formats.

This prevents a semantically correct answer expressed with the wrong JSON type from being conflated with a reasoning failure.
