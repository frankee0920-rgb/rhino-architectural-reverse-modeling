#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def load_json(path):
    if not path:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", required=True, choices=["L1","L2","L3"])
    ap.add_argument("--primary-reference", required=True)
    ap.add_argument("--model-capture", required=True)
    ap.add_argument("--comparison-dir")
    ap.add_argument("--dimensions-json")
    ap.add_argument("--hypothesis-json")
    ap.add_argument("--uncertainty-json")
    ap.add_argument("--checkpoint", default="")
    ap.add_argument("--out", default="review_packet.json")
    args = ap.parse_args()

    packet = {
        "review_level": args.level,
        "primary_reference": args.primary_reference,
        "model_capture": args.model_capture,
        "comparison_dir": args.comparison_dir,
        "dimensions": load_json(args.dimensions_json),
        "architecture_hypothesis": load_json(args.hypothesis_json),
        "uncertainties": load_json(args.uncertainty_json),
        "checkpoint": args.checkpoint,
        "review_instruction": "Use REVIEWER.md. Do not trust modeler justification. Find evidence-based errors."
    }
    Path(args.out).write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(Path(args.out).resolve())

if __name__ == "__main__":
    main()
