# GaiaGrid AI Benchmark

### Evaluating Large Language Models on Environmental Data Interpretation, Statistical Reasoning, and Evidence-Based Decision-Making

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Framework](https://img.shields.io/badge/Framework-Custom%20LLM%20Benchmark-green)
![Testing](https://img.shields.io/badge/Tests-12%20Passed-brightgreen)
![Tasks](https://img.shields.io/badge/Benchmark%20Tasks-8-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 1. Project Overview

GaiaGrid AI Benchmark is a Python-based evaluation framework designed to assess how effectively Large Language Models (LLMs) interpret environmental data, perform statistical reasoning, verify mathematical calculations, identify missing information, and make evidence-based decisions.

The project evaluates two language models:

- **GPT-OSS 120B** — `openai/gpt-oss-120b`
- **Qwen 3.8 27B** — `qwen/qwen3.8-27b`

Both models are evaluated using the same eight structured benchmark tasks.

The evaluation focuses on two primary dimensions:

1. **Semantic Correctness:** Whether the model provides a factually and logically correct response.
2. **Schema Compliance:** Whether the model follows the expected structured JSON output format and data types.

The framework retains raw model responses, calculates evaluation scores, and generates comparative results.

## 2. Project Objectives

The primary objectives are:

- Evaluate LLM performance on environmental data interpretation.
- Test statistical reasoning and mathematical accuracy.
- Assess the ability to distinguish correlation from causation.
- Evaluate how models handle missing or incomplete data.
- Test structured JSON generation and schema compliance.
- Compare model performance using consistent benchmark tasks.
- Provide reproducible evaluation artifacts and transparent scoring.

## 3. Problem Statement

Large Language Models can generate convincing explanations and answers, but their responses are not always factually correct, mathematically accurate, or structurally consistent.

This creates challenges when using LLMs in data-driven applications, particularly those involving environmental information and evidence-based decision-making.

GaiaGrid AI Benchmark addresses this problem by introducing structured evaluation tasks that test reasoning accuracy, numerical correctness, data interpretation, and output reliability.

Instead of evaluating models only through general conversational quality, the framework assesses their performance against predefined expected answers and evaluation criteria.

## 4. Benchmark Dataset

The benchmark uses a statewise NGO dataset containing information about active NGOs across Indian states and union territories.

**Dataset file:** `data/statewise_ngo.csv`

### Dataset characteristics

| Attribute | Description |
|---|---|
| Dataset subject | Statewise active NGO distribution |
| Number of records | 35 |
| Main data field | State Name |
| Numerical field | Active NGOs |
| Highest recorded value | Maharashtra — 66,913 |
| Lowest recorded value | Lakshadweep — 12 |
| Median | 6,132 |

### Data limitations

The original dataset contains NGO counts. It does not contain actual AQI readings or temperature measurements.

Therefore, environmental measurements are not treated as if they were present in the original dataset. Tasks involving environmental indicators use explicitly defined scenarios or supplied values.

This distinction is important for preventing models from inventing data or making unsupported conclusions.

## 5. Benchmark Tasks

The benchmark consists of eight structured tasks.

| Task ID | Task Name | Evaluation Focus |
|---|---|---|
| GG-001 | Dataset Interpretation | Identifying the state with the highest NGO count |
| GG-002 | Statistical Reasoning | Calculating and interpreting the median |
| GG-003 | AQI Interpretation | Understanding environmental index values |
| GG-004 | Mathematical Verification | Applying and verifying a custom mathematical formula |
| GG-005 | Correlation vs Causation | Identifying unsupported causal conclusions |
| GG-006 | Missing Data Handling | Recognizing unavailable environmental measurements |
| GG-007 | Min-Max Normalization | Understanding the effect of uniform positive scaling |
| GG-008 | Evidence-Based Decision Making | Making cautious decisions using available evidence |

### Mathematical formula

The benchmark includes a custom heuristic score:

\[
S = (0.40N + 0.35A + 0.25T)\times100
\]

Where:

- \(N\) = NGO-related normalized indicator
- \(A\) = Air-quality indicator
- \(T\) = Temperature-related indicator

For GG-004, the supplied values are:

\[
N=0.6,\quad A=0.8,\quad T=0.4
\]

Expected calculation:

\[
S=(0.40(0.6)+0.35(0.8)+0.25(0.4))\times100
\]

\[
S=(0.24+0.28+0.10)\times100
\]

\[
\boxed{S=62}
\]

This formula is a custom heuristic used for benchmark evaluation. It is not a scientifically validated environmental sustainability index.

## 6. System Architecture

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
              -----------------------
              |                     |
         GPT-OSS 120B          Qwen 3.8 27B
              |                     |
              -----------------------
                          |
                    Raw Responses
                          |
                  ----------------
                  |              |
                JSON             TXT
                  |              |
                  ----------------
                          |
                    Evaluator
                  evaluator.py
                          |
              -----------------------
              |                     |
       Semantic Evaluation    Schema Validation
              |                     |
              -----------------------
                          |
                    Final Scores
                          |
                  final_revised_scores.csv
                          |
                 Comparative Analysis
```

### Main components

**1. Benchmark Tasks**

`benchmark/tasks.json` contains the eight predefined evaluation tasks, expected answers, and grading criteria.

**2. Model Runner**

`src/model_runner.py` sends benchmark prompts to the selected language model through the Groq-compatible API endpoint and stores the generated responses.

**3. Evaluator**

`src/evaluator.py` evaluates responses using task-specific semantic checks and structured output validation.

**4. Rescoring Module**

`src/rescore_existing.py` reevaluates previously saved JSON responses using the current evaluator implementation.

**5. Test Suite**

`tests/test_evaluator.py` validates the evaluator's behavior, including numerical values, Boolean types, required concepts, and structured response fields.

## 7. Evaluation Methodology

Each model is evaluated against the same eight benchmark tasks.

The evaluation uses two separate metrics.

### A. Semantic Correctness

Semantic correctness measures whether the model's answer satisfies the expected answer and task-specific reasoning criteria.

Depending on the task, evaluation checks include:

- Numerical accuracy.
- Required concepts.
- Correct interpretation.
- Logical consistency.
- Appropriate handling of missing information.
- Evidence-based conclusions.

### B. Schema Compliance

Schema compliance measures whether the model follows the expected JSON structure and required data types.

The evaluator checks supported field types, including:

- Numeric values.
- Boolean values.
- Strings.
- Lists of strings.

For example, a Boolean field must contain an actual JSON Boolean (`true` or `false`), rather than a string such as `"true"`.

### C. Scoring

The benchmark reports semantic correctness and schema compliance separately.

The average score for each metric is calculated across the eight tasks:

\[
Average\ Score = \frac{\sum_{i=1}^{8} Score_i}{8}
\]

Keeping the two metrics separate helps distinguish reasoning quality from structured-output reliability.

## 8. Final Evaluation Results

The following results were obtained after applying the revised evaluator to the saved model responses.

### Model comparison

| Evaluation Metric | GPT-OSS 120B | Qwen 3.8 27B |
|---|---:|---:|
| Average Semantic Score | 75.00% | 81.25% |
| Average Schema Compliance | 100.00% | 93.75% |

### Key observations

**GPT-OSS 120B**

- Achieved 75.00% average semantic correctness.
- Achieved 100.00% average schema compliance.
- Demonstrated consistent adherence to the expected structured output format.
- Had weaker semantic results on several qualitative reasoning tasks.

**Qwen 3.8 27B**

- Achieved 81.25% average semantic correctness.
- Achieved 93.75% average schema compliance.
- Performed better on the overall semantic evaluation.
- Had errors in median calculation and mathematical verification.
- Returned a string instead of a JSON Boolean in one evaluated response.

### Overall interpretation

Qwen achieved a 6.25 percentage-point advantage in average semantic correctness.

GPT-OSS achieved a 6.25 percentage-point advantage in average schema compliance.

These results indicate different strengths across the evaluated tasks. They do not establish universal model superiority.

## 9. Project Structure

```text
GaiaGrid-AI-Benchmark/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── benchmark/
│   └── tasks.json
│
├── data/
│   └── statewise_ngo.csv
│
├── docs/
│   └── methodology.md
│
├── reports/
│   ├── evaluation_report.md
│   └── demo_script.md
│
├── src/
│   ├── __init__.py
│   ├── evaluator.py
│   ├── model_runner.py
│   └── rescore_existing.py
│
├── tests/
│   └── test_evaluator.py
│
└── results/
    ├── final_revised_scores.csv
    ├── initial_qwen_adjudication.md
    └── raw_outputs/
        ├── JSON responses
        └── TXT responses
```

## 10. Installation and Setup

### Prerequisites

- Python 3.11 or compatible version.
- pip.
- Groq API key.
- Git (optional).

### Step 1: Clone the repository

```bash
git clone https://github.com/harbhajanbhatiya/GaiaGrid-AI-Benchmark.git
cd GaiaGrid-AI-Benchmark
```

### Step 2: Create a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure the API key

Create a `.env` file in the project root.

Add:

```env
GROQ_API_KEY=your_actual_api_key
```

Never upload `.env` or expose your API key publicly.

The repository includes `.env.example` as a configuration template.

## 11. Running the Benchmark

Run the benchmark for GPT-OSS 120B:

```bash
python src/model_runner.py --model "openai/gpt-oss-120b"
```

Run the benchmark for Qwen 3.8 27B:

```bash
python src/model_runner.py --model "qwen/qwen3.8-27b"
```

The model runner stores raw responses in:

```text
results/raw_outputs/
```

The saved responses are evaluated and scoring results are generated by the runner.

### Recalculate scores

To reevaluate saved JSON responses using the current evaluator:

```bash
python src/rescore_existing.py
```

The revised results are saved in:

```text
results/final_revised_scores.csv
```

## 12. Running Tests

Execute:

```bash
python -m pytest -q
```

The current evaluator test suite reports:

```text
12 passed
```

These tests validate evaluator behavior. They do not independently establish the scientific validity of the benchmark or its scoring methodology.

## 13. Project Demonstration

A video walkthrough of the project is available below.

**Video Demonstration:**

https://youtu.be/-l6CUflgRZs

The demonstration covers the benchmark implementation, model evaluation process, and comparative results.

## 14. Reproducibility and Evidence

The repository provides:

- Benchmark task definitions.
- Original dataset.
- Model runner implementation.
- Evaluator implementation.
- Raw model responses in JSON and TXT formats.
- Revised evaluation scores.
- Unit tests.
- Evaluation methodology.
- Detailed evaluation report.

The reported results are based on one verified response set per model and task.

Duplicate copies of identical raw responses were not counted as independent experimental runs.

## 15. Limitations

The current benchmark has several limitations:

1. **Limited task coverage:** The evaluation contains eight benchmark tasks.
2. **Limited experimental repetitions:** Only one verified response set per model and task is established.
3. **Rule-based evaluation:** Semantic evaluation relies on predefined checks and concepts rather than comprehensive human assessment.
4. **Model-specific behavior:** Results may vary with model versions, prompting, generation settings, and API changes.
5. **Dataset limitations:** The NGO dataset does not contain actual AQI or temperature observations.
6. **Heuristic scoring:** The custom environmental formula is not a scientifically validated sustainability index.
7. **Limited generalization:** Results cannot be generalized to all LLM applications or reasoning tasks.

## 16. Future Improvements

Potential improvements include:

- Expanding the benchmark with more environmental reasoning tasks.
- Conducting multiple independent runs for each model and task.
- Introducing human-reviewed reference answers.
- Adding stronger semantic evaluation methods.
- Evaluating more language models.
- Measuring response consistency and reasoning reliability.
- Incorporating validated environmental datasets.
- Improving reproducibility through versioned model and API configurations.

## 17. Conclusion

GaiaGrid AI Benchmark provides a structured framework for evaluating language models on environmental data interpretation, statistical reasoning, mathematical verification, and evidence-based decision-making.

The evaluation of GPT-OSS 120B and Qwen 3.8 27B demonstrates that model performance can differ between semantic correctness and structured-output compliance.

Qwen achieved a higher average semantic score, while GPT-OSS achieved higher schema compliance.

The project establishes a starting point for more comprehensive and reproducible LLM benchmarking in environmental data applications.

---

## Author and Project

**Project:** GaiaGrid AI Benchmark

**Developer:** Harbhajan Singh Bhatiya

**GitHub:** https://github.com/harbhajanbhatiya/GaiaGrid-AI-Benchmark

**Demonstration:** https://youtu.be/-l6CUflgRZs

---

*GaiaGrid AI Benchmark — Evaluating reasoning, accuracy, and structured reliability in Large Language Models.*