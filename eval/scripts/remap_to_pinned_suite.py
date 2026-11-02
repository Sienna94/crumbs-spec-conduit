#!/usr/bin/env python3
"""채점 결과를 두 구현체가 고정한 공식 스펙 버전(realworld 450bbc5)의 정답지로 옮긴다 (표준 라이브러리만 사용).

채점자는 더 새로운 공식 스펙(2558884)을 기준으로 채점했다. 그 버전에는 이메일 형식을 검사하는
요청 세 개(errors_auth-04, errors_auth-10, errors_auth-15)가 더 있다. 두 버전의 요청 내용이 같은
행에는 채점 결과를 그대로 옮기고, 새 정답지에 없는 행은 eval/grading-newer-suite-extra.csv에 따로 남긴다.
"""
import argparse
import csv
import os
import sys
from collections import Counter

EVAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_FIELDS = ["file", "title", "kind", "method", "path", "auth", "body", "status", "asserts"]
GRADING_FIELDS = ["id", "verdict", "marked", "doc", "note"]
EXTRA_FIELDS = ["impl"] + GRADING_FIELDS
EXPECTED_UNMATCHED = {"errors_auth-04", "errors_auth-10", "errors_auth-15"}
EXTRA_NAME = "grading-newer-suite-extra.csv"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def key_of(row):
    return tuple(row[field] for field in KEY_FIELDS)


def behavior_index(rows):
    # 내용이 완전히 같은 요청이 한 파일에 두 번 있으면(errors_articles-14, -17) 등장 순서로 짝을 맞춘다.
    keyed = {}
    seen = Counter()
    for row in rows:
        if row["kind"] != "behavior":
            continue
        base = key_of(row)
        keyed[base + (seen[base],)] = row
        seen[base] += 1
    return keyed


def main():
    parser = argparse.ArgumentParser(description="채점 CSV를 고정 버전 정답지의 id로 옮긴다.")
    parser.add_argument("--old-ground-truth", required=True, help="이전 정답지 CSV (2558884 기준)")
    parser.add_argument("--old-grading", required=True, nargs="+", help="이전 채점 CSV (grading-<impl>.csv)")
    args = parser.parse_args()

    new_rows = read_rows(os.path.join(EVAL_DIR, "ground-truth.csv"))
    new_behaviors = behavior_index(new_rows)
    old_behaviors = behavior_index(read_rows(args.old_ground_truth))
    old_id_to_key = {row["id"]: key for key, row in old_behaviors.items()}
    new_ids = [row["id"] for row in new_rows if row["kind"] == "behavior"]

    results = {}
    extra_rows = []
    for path in args.old_grading:
        name = os.path.basename(path)
        if not (name.startswith("grading-") and name.endswith(".csv")):
            fail(f"채점 파일 이름이 grading-<impl>.csv 형식이 아니다: {name}")
        impl = name[len("grading-"):-len(".csv")]

        matched = {}
        for row in read_rows(path):
            old_id = row["id"]
            if old_id not in old_id_to_key:
                fail(f"{name}: 이전 정답지에 없는 id {old_id}")
            key = old_id_to_key[old_id]
            if key in new_behaviors:
                new_id = new_behaviors[key]["id"]
                if new_id in matched:
                    fail(f"{name}: {new_id} 행이 두 번 채점되어 있다")
                matched[new_id] = {field: row[field] for field in GRADING_FIELDS}
                matched[new_id]["id"] = new_id
            else:
                extra_rows.append({"impl": impl, **{field: row[field] for field in GRADING_FIELDS}})

        missing = [i for i in new_ids if i not in matched]
        if missing:
            fail(f"{impl}: 채점이 없는 정답지 행 {missing}")

        unmatched_ids = sorted(row["id"] for row in extra_rows if row["impl"] == impl)
        if unmatched_ids != sorted(EXPECTED_UNMATCHED):
            fail(f"{impl}: 옮기지 못한 행이 {unmatched_ids}이다 (기대: {sorted(EXPECTED_UNMATCHED)})")

        results[impl] = matched

    for impl, matched in results.items():
        with open(os.path.join(EVAL_DIR, f"grading-{impl}.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=GRADING_FIELDS)
            writer.writeheader()
            for new_id in new_ids:
                writer.writerow(matched[new_id])
        print(f"grading-{impl}.csv: {len(matched)}행")

    with open(os.path.join(EVAL_DIR, EXTRA_NAME), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EXTRA_FIELDS)
        writer.writeheader()
        writer.writerows(extra_rows)
    print(f"{EXTRA_NAME}: {len(extra_rows)}행")


if __name__ == "__main__":
    main()
