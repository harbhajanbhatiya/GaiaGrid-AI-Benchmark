# Methodology

## 1. Benchmark Design

GaiaGrid AI Benchmark evaluates the ability of language models to reason about environmental and statistical data through eight structured tasks.

The benchmark covers:

- Dataset retrieval and interpretation
- Descriptive statistical reasoning
- Categorical air-quality index interpretation
- Mathematical verification
- Correlation versus causation
- Missing-data handling
- Min-max normalization invariance
- Evidence-based environmental planning

Each task has a defined prompt, expected response structure, reference answer, and evaluation criteria.

## 2. Dataset and Ground Truth

The benchmark uses the state-wise NGO dataset available at:

`data/statewise_ngo.csv`

Dataset-based ground truth is derived from the supplied CSV, including state-level NGO counts, highest and lowest values, and descriptive statistics.

Synthetic tasks explicitly define their assumptions and input values.

Important distinctions:

- NGO counts are dataset observations.
- Synthetic environmental scenarios are not live measurements.
- Missing AQI and temperature values must not be fabricated or treated as evidence of good environmental conditions.
- The benchmark does not claim that NGO counts independently measure environmental quality.

## 3. Models Evaluated

Two language models were evaluated:

1. `openai/gpt-oss-120b`
2. `qwen/qwen3.8-27b`

Both models were evaluated against the same eight benchmark tasks.

This produced:
- 8 tasks per model.
- 2 evaluated models.
- 16 model responses in total.
- 1 verified response set per model per task.

The available results do not represent independent repeated trials.

## 4. Evaluation Methodology

The evaluator uses two separate dimensions.

### 4.1 Semantic Correctness

Semantic scoring measures whether the model's response satisfies the expected answer and task-specific evaluation criteria.

Depending on the field, the evaluator checks:

- Exact expected values.
- Numeric answers.
- Boolean meaning.
- Required concepts.
- Qualitative reasoning criteria.

Qualitative checks use transparent, rule-based keyword and concept matching.

### 4.2 Schema Compliance

Schema compliance evaluates whether the response follows the expected structured output requirements.

The improved evaluator validates:

- Numeric fields contain valid numeric values.
- Boolean fields contain actual JSON Boolean values.
- Text fields contain strings.
- List fields contain lists of strings.
- Required fields are present.
- Invalid types and missing fields do not receive schema credit.

Semantic correctness and schema compliance are evaluated independently. A response may communicate the correct meaning while still violating the required JSON structure.

### 4.3 Aggregate Scores

Task-level semantic and schema scores are aggregated using the arithmetic mean across the eight tasks.

The two dimensions are reported separately rather than being combined into an arbitrary overall score.

## 5. Evaluation Results

| Model | Average Semantic Score | Average Schema Compliance |
|---|---:|---:|
| openai/gpt-oss-120b | 75.00% | 100.00% |
| qwen/qwen3.8-27b | 81.25% | 93.75% |

### Key Observations

- Qwen achieved a higher average semantic score.
- GPT-OSS achieved higher schema compliance.
- GPT-OSS performed better on the statistical reasoning and mathematical verification tasks.
- Qwen performed better on correlation reasoning, missing-data handling, normalization, and evidence-based planning.
- Both models performed equally on dataset interpretation and AQI interpretation.

These findings describe performance on this specific benchmark and should not be generalized to all model capabilities.

## 6. Reproducibility and Data Integrity

The benchmark includes:

- Task definitions in `benchmark/tasks.json`.
- Source dataset in `data/statewise_ngo.csv`.
- Evaluation implementation in `src/evaluator.py`.
- Model execution implementation in `src/model_runner.py`.
- Automated evaluator tests in `tests/test_evaluator.py`.
- Saved model responses in `results/raw_outputs/`.
- Rescored evaluation results in `results/final_revised_scores.csv`.

The existing raw-output copies were compared using SHA-256 hashes. The compared copies were byte-identical and therefore do not establish independent repeated model runs.

The final reported results use one verified response per model per task.

## 7. Limitations

The benchmark has several limitations:

1. Only eight tasks are included.
2. Only two models were evaluated.
3. Only one verified response set per model per task is available.
4. Qualitative scoring relies partly on keyword and rule-based matching.
5. Automated scoring can produce false positives and false negatives.
6. The evaluator has not yet undergone comprehensive independent human validation.
7. The benchmark does not establish statistical significance or general model superiority.
8. The NGO dataset alone cannot establish environmental quality, NGO effectiveness, or actual environmental impact.

Consequently, the results should be interpreted as a preliminary comparative evaluation.

## 8. Future Improvements

Further development should focus on:

- Independent domain-expert review of tasks and reference answers.
- Human validation of qualitative model responses.
- Additional adversarial prompts and edge cases.
- Independent verification of all ground-truth values.
- Measurement of evaluator false-positive and false-negative rates.
- Multiple independent model runs to assess response stability.
- Evaluation of additional language models.
- Expansion of environmental datasets and real-world scenarios.
- Version control and freezing of benchmark tasks before comparative evaluations.

## 9. Conclusion

GaiaGrid AI Benchmark provides a reproducible, structured starting point for evaluating language-model performance on environmental data interpretation and reasoning tasks.

The initial comparison shows differences between semantic correctness and structured-output compliance. These results demonstrate why evaluating language models through multiple dimensions is more informative than relying on a single aggregate score.

The benchmark is preliminary and requires broader testing and independent validation before supporting general conclusions about model performance.
