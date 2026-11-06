"""Re-score already saved JSON model outputs with the current evaluator."""
import csv, json, re
from pathlib import Path
from evaluator import load_tasks, evaluate_response

def main():
    tasks = load_tasks("benchmark/tasks.json")
    raw_dir = Path("results/raw_outputs")
    rows = []
    for path in sorted(raw_dir.glob("*.json")):
        match = re.search(r"_(GG-\d{3})\.json$", path.name)
        if not match:
            continue
        task_id = match.group(1)
        task = next((t for t in tasks if t["task_id"] == task_id), None)
        if task is None:
            print(f"Skipping {path.name}: task not found in current task set")
            continue
        model = path.name[:-(len(task_id) + 6)]
        response = json.loads(path.read_text(encoding="utf-8"))
        result = evaluate_response(task, response)
        rows.append({
            "model": model.replace("_", "/", 1),
            "task_id": task_id,
            "semantic_score": result["semantic_score"],
            "schema_compliance_score": result["schema_compliance_score"],
            "field_results": json.dumps(result["field_results"], ensure_ascii=False)
        })
    if not rows:
        raise SystemExit("No matching JSON outputs found in results/raw_outputs/")
    out = Path("results/final_revised_scores.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Re-scored {len(rows)} responses. Results saved to {out}")
    print("These are automated rubric scores; manually review qualitative judgments before publication.")

if __name__ == "__main__":
    main()
