import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from evaluator import load_tasks, evaluate_response

ROOT = Path(__file__).resolve().parents[1]
TASKS = load_tasks(ROOT / "benchmark/tasks.json")

def task(task_id):
    return next(t for t in TASKS if t["task_id"] == task_id)

def test_gg004_corrected_ground_truth_is_62():
    t = task("GG-004")
    assert t["expected_answer"]["score"] == 62.0
    assert evaluate_response(t, {"score": 62.0})["semantic_score"] == 100.0

def test_gg003_accepts_equivalent_limitation_wording():
    t = task("GG-003")
    response = {"category":"Very Poor",
                "limitation":"This index is not a direct concentration measurement and must not be relabelled as the US EPA AQI."}
    assert evaluate_response(t, response)["semantic_score"] == 100.0

def test_gg005_accepts_reasoned_alternatives():
    t = task("GG-005")
    response = {"causal_claim_supported":False,
                "conclusion":"The data shows association but does not support a causal claim.",
                "two_alternative_explanations":["regional wealth and development differences",
                                               "reverse causality or different government regulation"]}
    assert evaluate_response(t, response)["semantic_score"] == 100.0

def test_gg006_accepts_missing_data_caution():
    t = task("GG-006")
    response = {"environmental_score_calculable":False,
                "action":"Request current AQI and temperature readings for the state.",
                "prohibited_assumption":"Assuming missing AQI and temperature values indicate good environmental conditions is not justified."}
    assert evaluate_response(t, response)["semantic_score"] == 100.0

def test_gg007_semantics_and_schema_are_separate():
    t = task("GG-007")
    response = {"normalized_values_change":"none",
                "explanation":"Min-max normalization is invariant to uniform positive scaling; the common factor cancels and normalized values are unchanged."}
    result = evaluate_response(t, response)
    assert result["semantic_score"] == 100.0
    assert result["schema_compliance_score"] == 50.0

def test_gg008_planning_rubric_accepts_capacity_wording():
    t = task("GG-008")
    response = {"state":"Lakshadweep","active_ngos":12,
                "planning_implication":"The limited number of registered entities may constrain local implementation capacity or require external partners for service delivery.",
                "evidence_limit":"The dataset only gives NGO counts and lacks population, geographic area, effectiveness and sector information."}
    assert evaluate_response(t, response)["semantic_score"] == 100.0

def test_wrong_median_still_fails():
    t = task("GG-002")
    result = evaluate_response(t, {"median_active_ngos":5107,"record_count":35})
    assert result["semantic_score"] == 50.0

def test_numeric_string_fails_strict_schema():
    t = task("GG-001")

    result = evaluate_response(
        t,
        {
            "state": "Maharashtra",
            "active_ngos": "66913"
        }
    )

    assert result["semantic_score"] == 50.0
    assert result["schema_compliance_score"] == 50.0


def test_boolean_string_has_semantics_but_not_schema():
    t = task("GG-007")

    result = evaluate_response(
        t,
        {
            "normalized_values_change": "false",
            "explanation": (
                "Uniform positive scaling leaves normalized "
                "values unchanged because the common factor cancels."
            )
        }
    )

    assert result["semantic_score"] == 100.0
    assert result["schema_compliance_score"] == 50.0


def test_boolean_is_not_accepted_as_number():
    t = task("GG-004")

    result = evaluate_response(
        t,
        {"score": True}
    )

    assert result["semantic_score"] == 0.0
    assert result["schema_compliance_score"] == 0.0


def test_list_field_rejects_string():
    t = task("GG-005")

    result = evaluate_response(
        t,
        {
            "causal_claim_supported": False,
            "conclusion": (
                "The association does not establish causation."
            ),
            "two_alternative_explanations": (
                "wealth and government regulation"
            )
        }
    )

    assert result["field_results"][
        "two_alternative_explanations"
    ]["schema_status"] == "fail"


def test_missing_field_fails_both_scores():
    t = task("GG-004")

    result = evaluate_response(t, {})

    assert result["semantic_score"] == 0.0
    assert result["schema_compliance_score"] == 0.0
