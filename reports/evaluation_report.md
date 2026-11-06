# GaiaGrid AI Benchmark
## Comprehensive Evaluation Report

**Project:** GaiaGrid AI Benchmark  
**Category:** Large Language Model Evaluation  
**Domain:** Environmental Data Interpretation and Reasoning  
**Models Evaluated:** GPT-OSS 120B and Qwen 3.8 27B  
**Benchmark Tasks:** 8  
**Evaluation Dimensions:** Semantic Correctness and Schema Compliance  
**Status:** Completed

---

# 1. Executive Summary

GaiaGrid AI Benchmark is a Python-based framework developed to evaluate the reasoning capabilities and structured-output reliability of Large Language Models (LLMs) in environmental data-related scenarios.

The benchmark focuses on evaluating whether models can correctly interpret datasets, perform statistical calculations, understand environmental indicators, verify mathematical formulas, distinguish correlation from causation, recognize missing information, and make evidence-based decisions.

Two language models were evaluated:

- GPT-OSS 120B (`openai/gpt-oss-120b`)
- Qwen 3.8 27B (`qwen/qwen3.8-27b`)

Both models were tested against eight predefined tasks using a common evaluation framework.

The evaluation considers two independent dimensions:

1. Semantic Correctness.
2. JSON Schema Compliance.

### Final Results

| Evaluation Metric | GPT-OSS 120B | Qwen 3.8 27B |
|---|---:|---:|
| Average Semantic Score | 75.00% | 81.25% |
| Average Schema Compliance | 100.00% | 93.75% |

The results show that Qwen achieved a higher average semantic score, while GPT-OSS achieved higher schema compliance.

These findings represent preliminary results from the evaluated tasks and should not be interpreted as a definitive ranking of the models.

# 2. Introduction

Large Language Models are increasingly used for data interpretation, analytical assistance, and decision-support applications.

However, a model producing a fluent answer does not necessarily mean that the answer is factually correct, mathematically accurate, or supported by available evidence.

In environmental applications, incorrect interpretations or unsupported assumptions can lead to misleading conclusions.

For this reason, evaluating LLMs requires more than measuring their ability to generate natural-language responses.

GaiaGrid AI Benchmark introduces a structured evaluation approach that focuses on reasoning accuracy, numerical verification, data interpretation, and structured-output reliability.

# 3. Problem Statement

Large Language Models may produce incorrect numerical calculations, misunderstand statistical information, make unsupported causal claims, or generate responses that do not follow the expected output structure.

These problems reduce the reliability of LLMs when they are used for analytical and data-driven applications.

The problem addressed by this project is:

**How can Large Language Models be systematically evaluated for their ability to interpret environmental data, perform analytical reasoning, verify numerical results, and produce reliable structured outputs?**

GaiaGrid AI Benchmark addresses this problem through predefined evaluation tasks, automated scoring, raw response collection, and comparative analysis.

# 4. Project Objectives

The objectives of the benchmark are:

1. Evaluate the interpretation of environmental and NGO-related data.
2. Assess statistical reasoning and numerical accuracy.
3. Test understanding of environmental indicators.
4. Verify mathematical calculations using predefined formulas.
5. Evaluate the ability to distinguish correlation from causation.
6. Test the handling of missing and incomplete information.
7. Assess understanding of normalization techniques.
8. Evaluate evidence-based decision-making.
9. Measure structured JSON output compliance.
10. Compare the performance of different LLMs using consistent evaluation criteria.

# 5. Dataset Description

The benchmark uses a statewise NGO dataset.

**Dataset location:** `data/statewise_ngo.csv`

The dataset contains information about active NGOs across Indian states and union territories.

### Dataset Summary

| Attribute | Value |
|---|---|
| Total records | 35 |
| State/UT field | State Name |
| Numerical field | Active NGOs |
| Highest NGO count | Maharashtra |
| Highest recorded count | 66,913 |
| Lowest NGO count | Lakshadweep |
| Lowest recorded count | 12 |
| Median NGO count | 6,132 |

### Dataset Limitations

The original dataset contains NGO counts only.

It does not contain actual AQI readings or temperature measurements.

Therefore, the benchmark distinguishes between:

- Values obtained from the original dataset.
- Values explicitly supplied in a benchmark scenario.
- Environmental observations that are not available.

This distinction prevents unsupported assumptions and fabricated environmental measurements.

# 6. Benchmark Design

The benchmark contains eight structured tasks.

Each task is designed to evaluate a specific analytical capability.

## 6.1 GG-001: Dataset Interpretation

**Objective:** Determine which state has the highest number of active NGOs.

**Expected Answer:** Maharashtra.

**Expected Value:** 66,913.

**Evaluation Focus:**

- Correct identification of the state.
- Accurate numerical interpretation.
- Avoiding unsupported conclusions.

## 6.2 GG-002: Statistical Reasoning

**Objective:** Evaluate the model's ability to interpret the dataset and calculate its median.

**Expected Answer:**

- Number of records: 35.
- Median: 6,132.

**Evaluation Focus:**

- Statistical calculation.
- Numerical accuracy.
- Correct interpretation of the dataset.

## 6.3 GG-003: AQI Interpretation

**Objective:** Evaluate the model's understanding of an OpenWeather-style air-quality index.

**Evaluation Focus:**

- Correct interpretation of the supplied index.
- Understanding that the index uses values from 1 to 5.
- Avoiding the assumption that it is a direct pollutant concentration.
- Avoiding confusion with the US EPA AQI scale.

## 6.4 GG-004: Mathematical Verification

**Objective:** Test the model's ability to apply a custom weighted scoring formula.

The formula is:

\[
S=(0.40N+0.35A+0.25T)\times100
\]

Given:

\[
N=0.6,\quad A=0.8,\quad T=0.4
\]

Calculation:

\[
S=(0.40\times0.6+0.35\times0.8+0.25\times0.4)\times100
\]

\[
S=(0.24+0.28+0.10)\times100
\]

\[
\boxed{S=62}
\]

**Expected Answer:** 62.

**Evaluation Focus:**

- Correct substitution.
- Arithmetic accuracy.
- Correct final result.

The formula is a custom benchmark heuristic, not a validated sustainability measurement.

## 6.5 GG-005: Correlation vs Causation

**Objective:** Evaluate whether the model understands the difference between correlation and causation.

**Expected Reasoning:**

An observed association does not independently establish a causal relationship.

Potential alternative explanations include:

- Economic differences.
- Urbanization.
- Government regulations.
- Industrial composition.
- Population distribution.

**Evaluation Focus:**

- Identifying unsupported causal claims.
- Recognizing alternative explanations.
- Demonstrating logical reasoning.

## 6.6 GG-006: Missing Data Handling

**Objective:** Evaluate the model's ability to recognize unavailable information.

**Expected Reasoning:**

The original dataset does not contain actual AQI and temperature measurements.

Therefore, a score requiring those unavailable inputs cannot be calculated from the original dataset alone.

Missing values must not automatically be interpreted as zero or as evidence of good environmental conditions.

**Evaluation Focus:**

- Missing data recognition.
- Avoiding fabricated values.
- Appropriate uncertainty handling.

## 6.7 GG-007: Min-Max Normalization

**Objective:** Evaluate understanding of min-max normalization under uniform positive scaling.

**Expected Reasoning:**

When all observations are multiplied by the same positive constant, their min-max normalized values remain unchanged, assuming the same non-degenerate dataset and normalization procedure.

**Evaluation Focus:**

- Understanding normalization.
- Mathematical reasoning.
- Correct interpretation of uniform scaling.

## 6.8 GG-008: Evidence-Based Decision-Making

**Objective:** Evaluate whether the model can make cautious decisions using the available NGO data.

**Expected Answer:**

Lakshadweep has the lowest recorded NGO count, with 12 active NGOs.

This may justify further investigation into local NGO presence and coverage.

However, NGO count alone does not establish environmental quality, NGO effectiveness, population needs, or actual service coverage.

**Evaluation Focus:**

- Correct identification of the lowest value.
- Evidence-based interpretation.
- Avoiding unsupported conclusions.

# 7. System Architecture

The benchmark follows a modular architecture.

```text
                  GaiaGrid AI Benchmark
                           |
                           |
                    Benchmark Tasks
                      tasks.json
                           |
                           |
                      Model Runner
                    model_runner.py
                           |
              -------------------------
              |                       |
         GPT-OSS 120B            Qwen 3.8 27B
              |                       |
              -------------------------
                           |
                     Raw Responses
                           |
                 ---------------------
                 |                   |
                JSON                 TXT
                 |                   |
                 ---------------------
                           |
                        Evaluator
                     evaluator.py
                           |
                -----------------------
                |                     |
          Semantic Checks       Schema Validation
                |                     |
                -----------------------
                           |
                    Revised Scores
                           |
             final_revised_scores.csv
                           |
                 Comparative Analysis
```

## 7.1 Main Components

### Benchmark Task Definitions

File: `benchmark/tasks.json`

Contains task descriptions, expected answers, and evaluation criteria.

### Model Runner

File: `src/model_runner.py`

Responsible for sending prompts to the selected language model through the configured API endpoint and retaining the generated responses.

### Evaluator

File: `src/evaluator.py`

Responsible for evaluating model responses using task-specific semantic checks and schema validation.

### Rescoring Module

File: `src/rescore_existing.py`

Allows previously saved JSON responses to be reevaluated using the revised evaluator.

### Unit Tests

File: `tests/test_evaluator.py`

Contains automated tests for evaluator behavior, including numerical validation, data types, and structured response checks.

# 8. Evaluation Methodology

Both models were evaluated using the same eight benchmark tasks.

The evaluation was conducted using two separate dimensions.

## 8.1 Semantic Correctness

Semantic correctness measures whether a model's response satisfies the expected answer and task-specific reasoning criteria.

Depending on the task, evaluation includes:

- Correct numerical values.
- Required concepts.
- Logical consistency.
- Correct interpretation.
- Appropriate handling of missing information.
- Evidence-based conclusions.

The semantic score is calculated from the applicable task-specific checks.

## 8.2 Schema Compliance

Schema compliance measures whether the model generates structured responses in the expected JSON format.

The evaluator checks field types, including:

| Expected Type | Validation |
|---|---|
| Number | Integer or floating-point value, excluding Boolean values |
| Boolean | Actual Boolean value |
| String | Valid string |
| List | List containing strings |

For example:

Valid:

```json
{
  "is_correct": true
}
```

Invalid:

```json
{
  "is_correct": "true"
}
```

Although both may communicate a similar meaning to a human reader, the second example does not satisfy a Boolean schema requirement.

## 8.3 Average Score Calculation

The average score for each metric is calculated across eight tasks:

\[
Average=\frac{\sum_{i=1}^{8}Score_i}{8}
\]

Semantic correctness and schema compliance are reported separately.

This avoids hiding differences between reasoning performance and structured-output reliability.

# 9. Experimental Results

The final revised evaluation results contain 16 records:

- Eight task evaluations for GPT-OSS 120B.
- Eight task evaluations for Qwen 3.8 27B.

## 9.1 Semantic Score Comparison

| Task ID | GPT-OSS 120B | Qwen 3.8 27B |
|---|---:|---:|
| GG-001 | 100.00% | 100.00% |
| GG-002 | 100.00% | 50.00% |
| GG-003 | 100.00% | 100.00% |
| GG-004 | 100.00% | 0.00% |
| GG-005 | 33.33% | 100.00% |
| GG-006 | 66.67% | 100.00% |
| GG-007 | 50.00% | 100.00% |
| GG-008 | 50.00% | 100.00% |
| **Average** | **75.00%** | **81.25%** |

## 9.2 Schema Compliance Comparison

| Model | Average Schema Compliance |
|---|---:|
| GPT-OSS 120B | 100.00% |
| Qwen 3.8 27B | 93.75% |

## 9.3 Overall Comparison

| Metric | GPT-OSS 120B | Qwen 3.8 27B |
|---|---:|---:|
| Semantic Correctness | 75.00% | 81.25% |
| Schema Compliance | 100.00% | 93.75% |

### Key Findings

**Finding 1: Qwen achieved a higher semantic score.**

Qwen achieved an average semantic score of 81.25%, compared with 75.00% for GPT-OSS.

The difference is 6.25 percentage points.

**Finding 2: GPT-OSS achieved higher schema compliance.**

GPT-OSS achieved 100.00% schema compliance, while Qwen achieved 93.75%.

This indicates stronger adherence to the expected structured output format in the evaluated responses.

**Finding 3: Numerical reasoning remains an area for improvement.**

Qwen produced an incorrect median for GG-002.

The expected median was 6,132, while the model returned 5,107.

**Finding 4: Mathematical verification exposed a model-specific error.**

For GG-004, the correct result was 62.

Qwen returned 64, demonstrating that fluent explanations do not guarantee correct arithmetic.

**Finding 5: Structured output and semantic quality are different evaluation dimensions.**

A model can follow the required JSON structure while providing an incorrect answer. Similarly, a response may communicate a semantically correct answer but fail a strict data-type requirement.

This supports evaluating both dimensions independently.

# 10. Evidence Integrity and Reproducibility

The project retains raw model responses in JSON and TXT formats.

The canonical response directory is:

```text
results/raw_outputs/
```

It contains:

- 16 JSON responses.
- 16 TXT responses.

The duplicate response directories were compared using SHA256 hashes.

The compared copies were byte-identical across the 16 response filenames.

Therefore, the duplicate directories represent copies of the same response set and are not treated as independent experimental runs.

The final revised score file is:

```text
results/final_revised_scores.csv
```

The revised scores were generated by applying the current evaluator to the retained JSON responses.

The repository also contains:

- Original benchmark tasks.
- Dataset.
- Model runner.
- Evaluator.
- Rescoring script.
- Unit tests.
- Methodology documentation.
- Evaluation results.

These artifacts allow reviewers to inspect the evaluation process and its outputs.

# 11. Testing and Validation

The evaluator was tested using the project's automated test suite.

Command:

```bash
python -m pytest -q
```

Result:

```text
12 passed
```

The tests cover evaluator behavior, including:

- Numeric type validation.
- Boolean type validation.
- String validation.
- List validation.
- Semantic evaluation checks.
- Structured response validation.

Passing unit tests indicates that the tested evaluator behavior works as expected.

It does not independently prove that the evaluation criteria are scientifically valid or that the benchmark generalizes to other models and tasks.

# 12. Limitations

The current benchmark has several limitations.

## 12.1 Limited Task Coverage

The benchmark contains eight tasks. This is a small evaluation set and cannot represent the full range of environmental reasoning capabilities.

## 12.2 Limited Independent Repetitions

The reported results represent one verified response set per model and task.

Independent repeated runs have not been established.

Consequently, the benchmark does not measure response variability or statistical significance.

## 12.3 Rule-Based Semantic Evaluation

The evaluator uses predefined semantic checks and task-specific criteria.

Such methods can miss valid alternative answers or fail to recognize subtle reasoning errors.

Human-reviewed evaluation would improve reliability.

## 12.4 Dataset Limitations

The original NGO dataset does not contain actual AQI or temperature measurements.

The benchmark therefore cannot establish real-world environmental conditions from NGO counts alone.

## 12.5 Custom Heuristic Formula

The weighted formula used in the benchmark is a custom heuristic.

Its weights and assumptions have not been scientifically validated as a sustainability measurement.

## 12.6 Model and API Variability

Model responses may vary with model versions, API changes, generation settings, and prompt configurations.

The reported scores should therefore be interpreted in the context of the evaluated model configurations and retained responses.

## 12.7 Limited Generalization

The results should not be generalized to all LLM applications, all reasoning tasks, or all environmental decision-making scenarios.

# 13. Future Scope

The following improvements could strengthen the benchmark.

1. Increase the number and diversity of benchmark tasks.
2. Conduct multiple independent runs for every model and task.
3. Introduce human-reviewed reference answers.
4. Improve semantic evaluation using stronger validation techniques.
5. Evaluate additional open-source and commercial language models.
6. Measure response consistency across repeated runs.
7. Add validated environmental datasets containing actual AQI and temperature measurements.
8. Introduce confidence intervals and statistical comparisons when sufficient repeated observations are available.
9. Track model versions, prompt configurations, and generation parameters.
10. Improve automated reporting and visualization of benchmark results.

# 14. Conclusion

GaiaGrid AI Benchmark provides a structured framework for evaluating Large Language Models on environmental data interpretation, statistical reasoning, mathematical verification, missing data handling, and evidence-based decision-making.

The evaluation compared GPT-OSS 120B and Qwen 3.8 27B across eight predefined tasks.

The results showed that Qwen achieved a higher average semantic score of 81.25%, while GPT-OSS achieved 100.00% average schema compliance.

These findings demonstrate that semantic correctness and structured-output reliability are distinct aspects of model performance.

The benchmark also highlights the importance of numerical verification, transparent evidence handling, and cautious interpretation of incomplete datasets.

Although the current evaluation is limited in scale, it provides a foundation for developing more comprehensive, repeatable, and reliable LLM evaluation frameworks.

# 15. Project Demonstration

**Video Demonstration:**

https://youtu.be/-l6CUflgRZs

The demonstration presents the benchmark workflow, model evaluation process, implementation, and comparative results.

# 16. Project Resources

**GitHub Repository:**

https://github.com/harbhajanbhatiya/GaiaGrid-AI-Benchmark

**Video Demonstration:**

https://youtu.be/-l6CUflgRZs

**Main Project Files:**

- `benchmark/tasks.json`
- `data/statewise_ngo.csv`
- `src/model_runner.py`
- `src/evaluator.py`
- `src/rescore_existing.py`
- `tests/test_evaluator.py`
- `results/final_revised_scores.csv`

---

**Project:** GaiaGrid AI Benchmark  
**Developer:** Harbhajan Singh Bhatiya  
**Domain:** Artificial Intelligence, Large Language Models, and Environmental Data Evaluation