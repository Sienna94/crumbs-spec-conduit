#!/usr/bin/env python3
"""Summarize the grading CSVs into eval/summary.md (standard library only)."""
import csv
import os
import sys

EVAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMPLS = ["nitro", "django"]


def read_csv(name):
    with open(os.path.join(EVAL_DIR, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def table(header_line, rows):
    lines = [header_line, "|" + "---|" * (header_line.count("|") - 1)]
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def main():
    truth = read_csv("ground-truth.csv")
    behavior_ids = [r["id"] for r in truth if r["kind"] == "behavior"]
    behavior_set = set(behavior_ids)

    grading = {}
    policies = {}
    for impl in IMPLS:
        rows = read_csv(f"grading-{impl}.csv")
        ids = [r["id"] for r in rows]
        if len(ids) != len(set(ids)):
            fail(f"grading-{impl}.csv has duplicate ids")
        if set(ids) != behavior_set:
            missing = sorted(behavior_set - set(ids))
            extra = sorted(set(ids) - behavior_set)
            fail(f"grading-{impl}.csv ids differ from ground truth: missing {missing}, extra {extra}")
        grading[impl] = {r["id"]: r for r in rows}
        policies[impl] = read_csv(f"policies-{impl}.csv")

    scored_ids = behavior_ids

    def suite_stats(impl):
        rows = [grading[impl][i] for i in scored_ids]
        return [
            len(rows),
            sum(r["verdict"] == "correct" for r in rows),
            sum(r["verdict"] == "partial" for r in rows),
            sum(r["verdict"] == "wrong" for r in rows),
            sum(r["verdict"] == "missing" for r in rows),
            sum(r["verdict"] == "correct" and r["marked"] == "question" for r in rows),
        ]

    def policy_stats(impl):
        rows = policies[impl]
        return [
            len(rows),
            sum(r["marked"] == "confirmed" for r in rows),
            sum(r["marked"] == "question" for r in rows),
            sum(r["supported"] == "yes" for r in rows),
            sum(r["supported"] == "partly" for r in rows),
            sum(r["supported"] == "no" for r in rows),
            sum(r["in_suite"] == "yes" for r in rows),
            sum(r["marked"] == "question" and r["in_suite"] == "yes" for r in rows),
        ]

    suite_labels = [
        "scored rows",
        "correct",
        "partial",
        "wrong",
        "missing",
        "correct while relying on a [needs confirmation] statement",
    ]
    policy_labels = [
        "policies",
        "confirmed",
        "question",
        "supported: yes",
        "supported: partly",
        "supported: no",
        "asserted by the suite (in_suite yes)",
        "questions asserted by the suite",
    ]

    suite_cols = {impl: suite_stats(impl) for impl in IMPLS}
    policy_cols = {impl: policy_stats(impl) for impl in IMPLS}

    out = []
    out.append("# Summary")
    out.append("")
    out.append("## Suite rows")
    out.append("")
    out.append(table("| | nitro | django |",
                     [[label, suite_cols["nitro"][k], suite_cols["django"][k]]
                      for k, label in enumerate(suite_labels)]))
    out.append("")
    out.append("## Policies")
    out.append("")
    out.append(table("| | nitro | django |",
                     [[label, policy_cols["nitro"][k], policy_cols["django"][k]]
                      for k, label in enumerate(policy_labels)]))
    out.append("")
    out.append("## Rows only in the newer suite (not scored)")
    out.append("")
    for r in read_csv("grading-newer-suite-extra.csv"):
        out.append(f"- `{r['id']}` {r['impl']} `{r['verdict']}`, {r['note']}")
    out.append("")
    out.append("## Rows where the two implementations differ")
    out.append("")
    diff_rows = [[i, grading["nitro"][i]["verdict"], grading["django"][i]["verdict"]]
                 for i in scored_ids
                 if grading["nitro"][i]["verdict"] != grading["django"][i]["verdict"]]
    out.append(table("| id | nitro | django |", diff_rows))

    text = "\n".join(out) + "\n"
    with open(os.path.join(EVAL_DIR, "summary.md"), "w", encoding="utf-8") as f:
        f.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
