import json
import math
import re
from pathlib import Path
from typing import Any


def _norm(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value).strip().lower())


def _contains_any(text: str, phrases: list[str]) -> bool:
    return any(p in text for p in phrases)


def _qualitative_check(field: str, actual: Any) -> bool:
    if not isinstance(actual, str):
        return False

    text = _norm(actual)

    rules = {
        "limitation": [
            [
                "not a direct concentration",
                "not a direct measurement",
                "not a concentration measurement"
            ],
            [
                "not be relabelled as the us epa aqi",
                "not the us epa aqi",
                "not equivalent to the us epa aqi",
                "not the epa aqi"
            ]
        ],
        "conclusion": [
            [
                "does not support a causal",
                "does not establish",
                "cannot establish",
                "does not prove",
                "not establish caus"
            ]
        ],
        "action": [
            ["request", "obtain", "collect", "retrieve"],
            ["aqi", "air quality"],
            ["temperature", "temp"]
        ],
        "prohibited_assumption": [
            ["missing", "absent", "unavailable"],
            ["assum", "imput", "invent", "treat"],
            ["good", "healthy", "zero", "neutral"]
        ],
        "explanation": [
            [
                "uniform positive scaling",
                "uniform scaling",
                "same positive factor",
                "multiplied by a constant"
            ],
            ["cancel", "cancels", "simplif", "invariant"],
            ["unchanged", "identical", "same normalized"]
        ],
        "planning_implication": [
            [
                "limited number",
                "low number",
                "small number",
                "few registered"
            ],
            [
                "capacity",
                "implementation",
                "external partners",
                "service delivery",
                "coverage"
            ]
        ],
        "evidence_limit": [
            ["count", "counts"],
            [
                "effectiveness",
                "population",
                "geographic",
                "sector",
                "environmental quality"
            ]
        ]
    }

    groups = rules.get(field)
    return bool(groups) and all(
        _contains_any(text, group) for group in groups
    )


def _numeric(
    actual: Any,
    expected: Any,
    tolerance: float = 1e-9
) -> bool:
    if isinstance(actual, bool):
        return False

    if not isinstance(actual, (int, float)):
        return False

    try:
        return (
            math.isfinite(float(actual))
            and math.isclose(
                float(actual),
                float(expected),
                rel_tol=0,
                abs_tol=tolerance
            )
        )
    except (TypeError, ValueError, OverflowError):
        return False


def _semantic_boolean(
    actual: Any,
    expected: bool
) -> tuple[bool, bool]:
    if isinstance(actual, bool):
        return actual is expected, True

    if isinstance(actual, str):
        equivalents = {
            "false": False,
            "no": False,
            "none": False,
            "unchanged": False,
            "true": True,
            "yes": True,
            "changed": True
        }

        text = _norm(actual)

        if text in equivalents:
            return equivalents[text] is expected, False

    return False, False


def _schema_type_ok(rule: str, actual: Any) -> bool:
    if rule in {
        "exact_numeric",
        "numeric_tolerance_0_01"
    }:
        return (
            isinstance(actual, (int, float))
            and not isinstance(actual, bool)
            and math.isfinite(float(actual))
        )

    if rule == "exact_boolean":
        return isinstance(actual, bool)

    if rule in {
        "exact_case_insensitive",
        "required_concepts"
    }:
        return isinstance(actual, str)

    if rule == "at_least_two_relevant":
        return (
            isinstance(actual, list)
            and all(isinstance(item, str) for item in actual)
        )

    return False


def evaluate_response(task: dict, response: dict) -> dict:
    expected = task["expected_answer"]
    rules = task["scoring"]

    details = {}
    semantic_points = 0.0
    schema_points = 0.0

    if not isinstance(response, dict):
        raise TypeError("Response must be a JSON object.")

    for field, rule in rules.items():

        if field not in response:
            details[field] = {
                "semantic_status": "missing",
                "semantic_score": 0.0,
                "schema_status": "missing",
                "schema_score": 0.0
            }
            continue

        actual = response[field]

        schema_ok = _schema_type_ok(rule, actual)

        if rule == "exact_case_insensitive":
            semantic_ok = (
                isinstance(actual, str)
                and _norm(actual) == _norm(expected[field])
            )

        elif rule == "exact_numeric":
            semantic_ok = _numeric(
                actual,
                expected[field]
            )

        elif rule == "numeric_tolerance_0_01":
            semantic_ok = _numeric(
                actual,
                expected[field],
                0.01
            )

        elif rule == "exact_boolean":
            semantic_ok, _ = _semantic_boolean(
                actual,
                expected[field]
            )

        elif rule == "required_concepts":
            semantic_ok = _qualitative_check(
                field,
                actual
            )

        elif rule == "at_least_two_relevant":
            if isinstance(actual, list) and all(
                isinstance(item, str) for item in actual
            ):
                joined = _norm(" ".join(actual))

                candidates = [
                    [
                        "wealth",
                        "income",
                        "development",
                        "urbanization",
                        "urbanisation"
                    ],
                    [
                        "government",
                        "regulation",
                        "policy",
                        "industrial",
                        "industry",
                        "reverse causality",
                        "reverse cause"
                    ]
                ]

                semantic_ok = (
                    len(actual) >= 2
                    and all(
                        _contains_any(joined, group)
                        for group in candidates
                    )
                )
            else:
                semantic_ok = False

        else:
            semantic_ok = False
            schema_ok = False

        details[field] = {
            "semantic_status": (
                "pass" if semantic_ok else "fail"
            ),
            "semantic_score": (
                1.0 if semantic_ok else 0.0
            ),
            "schema_status": (
                "pass" if schema_ok else "fail"
            ),
            "schema_score": (
                1.0 if schema_ok else 0.0
            )
        }

        semantic_points += float(semantic_ok)
        schema_points += float(schema_ok)

    count = max(len(rules), 1)

    return {
        "task_id": task["task_id"],
        "semantic_score": round(
            100 * semantic_points / count, 2
        ),
        "schema_compliance_score": round(
            100 * schema_points / count, 2
        ),
        "field_results": details,
        "grading_note": (
            "Qualitative keyword rubrics are screening aids; "
            "borderline cases require human adjudication."
        )
    }


def load_tasks(path: str | Path) -> list[dict]:
    return json.loads(
        Path(path).read_text(encoding="utf-8")
    )


def evaluate_json_file(
    task_id: str,
    response_path: str | Path,
    tasks_path: str | Path
) -> dict:
    tasks = load_tasks(tasks_path)

    task = next(
        (t for t in tasks if t["task_id"] == task_id),
        None
    )

    if task is None:
        raise ValueError(f"Unknown task_id: {task_id}")

    response = json.loads(
        Path(response_path).read_text(encoding="utf-8")
    )

    return evaluate_response(task, response)