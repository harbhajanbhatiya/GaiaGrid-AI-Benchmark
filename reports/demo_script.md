# GaiaGrid AI Benchmark
## Five-Minute Project Demonstration

### 00:00–00:35 — Introduction

Hello everyone.

Today, I am presenting GaiaGrid AI Benchmark, a structured framework designed to evaluate the reliability of language models when working with environmental data, mathematical calculations, statistical reasoning, and evidence-based decisions.

The primary objective is to go beyond simply checking whether an AI model generates an answer and evaluate whether that answer is correct and follows the required structure.

### 00:35–01:15 — Problem Statement

Language models can generate convincing responses, but convincing responses are not necessarily accurate.

They may produce incorrect calculations, misunderstand statistical information, make unsupported assumptions, or return invalid structured data.

Our benchmark addresses this problem by testing models against predefined tasks with expected answers and automated evaluation criteria.

### 01:15–02:00 — Benchmark Architecture

The project is implemented using Python.

It contains four major components:

First, a state-wise NGO dataset containing 35 records.

Second, eight benchmark tasks covering dataset interpretation, statistical reasoning, AQI interpretation, mathematical verification, correlation versus causation, missing data, normalization, and evidence-based planning.

Third, a model runner that communicates with language models through a Groq-compatible API.

Finally, an evaluator that compares model responses against predefined evaluation criteria.

### 02:00–02:45 — Evaluation Methodology

We evaluated two models:

GPT-OSS 120B and Qwen 3.8 27B.

Each model received the same eight benchmark tasks.

Our evaluator measures two independent dimensions.

Semantic correctness determines whether the response satisfies the expected answer and reasoning criteria.

Schema compliance checks whether the response follows the required JSON structure and data types.

This separation is important because a model can communicate the correct meaning while still returning an invalid data structure.

### 02:45–03:45 — Results and Comparison

Now let's examine the results.

GPT-OSS achieved an average semantic score of 75% and schema compliance of 100%.

Qwen achieved an average semantic score of 81.25% and schema compliance of 93.75%.

Qwen performed better in several qualitative reasoning tasks, including correlation versus causation, missing-data handling, normalization, and evidence-based planning.

GPT-OSS performed better in statistical reasoning and mathematical verification.

The results show that neither model dominates both dimensions.

### 03:45–04:30 — Validation and Reproducibility

We also implemented automated tests for the evaluator.

The current test suite contains 12 passing tests.

We retained raw model responses and generated a separate final scoring file.

We also compared available raw-output copies using SHA-256 hashes to check data integrity.

One important limitation is that the available responses represent one verified response set per model per task, not independent repeated experiments.

### 04:30–05:00 — Conclusion

To conclude, GaiaGrid AI Benchmark demonstrates how language models can be evaluated across multiple dimensions rather than relying on a single accuracy score.

The current results are preliminary, and future work will focus on additional tasks, more models, independent human validation, and repeated experiments.

Thank you.