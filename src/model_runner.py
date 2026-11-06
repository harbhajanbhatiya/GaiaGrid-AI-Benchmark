"""Run benchmark tasks with Groq and automatically score JSON responses."""
import os, json, argparse, csv, datetime
from pathlib import Path
import requests
import pandas as pd
from evaluator import load_tasks, evaluate_response

API_URL = "https://api.groq.com/openai/v1/chat/completions"

def enrich_input(task):
    data = dict(task["input_data"])
    dataset_file = data.get("dataset_file")
    if dataset_file:
        frame = pd.read_csv(dataset_file)
        data["dataset_records"] = frame.to_dict(orient="records")
        data["dataset_record_count"] = len(frame)
    return data

def run_task(task, model, api_key):
    system = ("Answer only with one valid JSON object. No Markdown fences or extra text. "
              "Use only the supplied evidence; state uncertainty rather than inventing facts.")
    user = task["prompt"] + "\n\nInput data:\n" + json.dumps(enrich_input(task), ensure_ascii=False)
    payload = {"model": model, "temperature": 0,
               "messages":[{"role":"system","content":system},{"role":"user","content":user}]}
    r = requests.post(API_URL, headers={"Authorization":f"Bearer {api_key}",
        "Content-Type":"application/json"}, json=payload, timeout=90)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def parse_json_response(raw):
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3]
    return json.loads(text.strip())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Exact model ID supported by your Groq account")
    parser.add_argument("--task-id", help="Optional task ID; defaults to all tasks")
    args = parser.parse_args()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise SystemExit("Set GROQ_API_KEY as an environment variable; never put it in source files.")
    tasks = load_tasks("benchmark/tasks.json")
    selected = [t for t in tasks if not args.task_id or t["task_id"] == args.task_id]
    if args.task_id and not selected:
        raise SystemExit(f"Unknown task ID: {args.task_id}")
    out_dir = Path("results/raw_outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for task in selected:
        raw = run_task(task, args.model, key)
        stem = f'{args.model.replace("/", "_")}_{task["task_id"]}'
        (out_dir / f"{stem}.txt").write_text(raw, encoding="utf-8")
        try:
            parsed = parse_json_response(raw)
            (out_dir / f"{stem}.json").write_text(json.dumps(parsed, indent=2), encoding="utf-8")
            result = evaluate_response(task, parsed)
            status = "scored"
        except Exception as exc:
            result = {"task_id": task["task_id"], "score": 0.0,
                      "field_results": {"response_format": {"score": 0.0, "status": f"invalid JSON: {exc}"}}}
            status = "invalid_json"
        rows.append({"model": args.model, "task_id": task["task_id"],
                     "score": result.get("semantic_score", result.get("score", 0)),
                    "semantic_score": result.get("semantic_score", result.get("score", 0)),
                    "schema_compliance_score": result.get("schema_compliance_score", 0),
                    "status": status,
                     "field_results": json.dumps(result["field_results"], ensure_ascii=False)})
        score = result.get("semantic_score", result.get("score", 0))
        print(f'{task["task_id"]}: {score:.2f}/100 ({status})')
    score_file = Path("results/scores.csv")
    score_file.parent.mkdir(parents=True, exist_ok=True)
    exists = score_file.exists()
    with score_file.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if not exists: writer.writeheader()
        writer.writerows(rows)
    print(f"Saved raw outputs to {out_dir} and scores to {score_file}")
    print("Record the exact model ID and run date when reporting results.")

if __name__ == "__main__":
    main()
