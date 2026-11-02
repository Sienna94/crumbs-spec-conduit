#!/usr/bin/env python3
"""Hurl API 테스트 파일을 요청 블록 단위 체크리스트(CSV)와 요약(Markdown)으로 변환한다.

사용법:
    python3 hurl_to_checklist.py [--input-dir DIR] [--output-dir DIR]

기본 입력은 vendor/realworld/specs/api/hurl, 기본 출력은 이 스크립트의 상위 디렉터리(eval/)다.
표준 라이브러리만 사용한다.
"""

import argparse
import csv
import glob
import json
import os
import re
import sys
from collections import Counter, OrderedDict

DEFAULT_INPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "vendor", "realworld", "specs", "api", "hurl",
)

METHOD_RE = re.compile(r"^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(\S+)\s*$")
HTTP_RE = re.compile(r"^HTTP\s+(\S+)\s*$")
HEADER_RE = re.compile(r"^([A-Za-z][A-Za-z0-9-]*):\s*(.*)$")
SECTION_RE = re.compile(r"^\[([A-Za-z]+)\]\s*$")
TOKEN_RE = re.compile(r"^Token \{\{[A-Za-z0-9_]+\}\}$")

COLUMNS = ["id", "file", "title", "kind", "method", "path", "auth", "body", "status", "asserts"]


class Warnings:
    def __init__(self):
        self.items = []

    def add(self, msg):
        self.items.append(msg)


def compact_body(raw, where, warns):
    """JSON 본문을 한 줄로 압축한다. JSON이 아니면 공백만 정리하고 경고를 남긴다."""
    if not raw:
        return ""
    try:
        obj = json.loads(raw, object_pairs_hook=OrderedDict)
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    except ValueError:
        warns.add(f"{where}: JSON 파싱 실패, 공백만 정리함")
        return " ".join(raw.split())


def parse_block(lines, start, file_name, warns):
    """start 줄의 메서드 라인부터 블록 하나를 파싱한다.

    반환값: (블록 dict, 블록 다음 줄 인덱스). 다음 블록의 주석 줄은 소비하지 않는다.
    """
    n = len(lines)
    m = METHOD_RE.match(lines[start].strip())
    method, url = m.group(1), m.group(2)
    where = f"{file_name}:{start + 1}"

    # HTTP 라인 위치 찾기 (헤더와 본문은 HTTP 라인 전까지)
    h = start + 1
    while h < n and not HTTP_RE.match(lines[h].strip()):
        if METHOD_RE.match(lines[h].strip()) or lines[h].startswith("#"):
            warns.add(f"{where}: HTTP 라인 없이 다음 블록이 시작됨")
            return None, h
        h += 1
    if h >= n:
        warns.add(f"{where}: HTTP 라인을 찾지 못함")
        return None, n

    status = HTTP_RE.match(lines[h].strip()).group(1)

    # 헤더와 본문 분리
    headers = []
    body_lines = []
    in_body = False
    for line in lines[start + 1:h]:
        s = line.strip()
        if not in_body:
            if s == "":
                continue
            if s.startswith("{") or s.startswith("["):
                in_body = True
                body_lines.append(line)
                continue
            hm = HEADER_RE.match(s)
            if hm:
                headers.append((hm.group(1), hm.group(2).strip()))
            else:
                warns.add(f"{where}: 알 수 없는 헤더/라인 `{s}`")
        else:
            body_lines.append(line)
    raw_body = "\n".join(body_lines).strip()

    auth = "none"
    for name, value in headers:
        if name.lower() == "authorization":
            auth = "token" if TOKEN_RE.match(value) else value
            break

    # 응답 섹션 ([Asserts], [Captures]) 파싱. 주석이나 다음 메서드 라인에서 블록이 끝난다.
    asserts = []
    section = None
    k = h + 1
    while k < n:
        line = lines[k]
        s = line.strip()
        if METHOD_RE.match(s) or line.startswith("#"):
            break
        if s == "":
            k += 1
            continue
        sm = SECTION_RE.match(s)
        if sm:
            section = sm.group(1).lower()
        elif section == "asserts":
            asserts.append(s)
        elif section is None:
            warns.add(f"{where}: HTTP 뒤 섹션 없는 라인 `{s}`")
        k += 1

    path = url.replace("{{host}}", "")
    if not path.startswith("/"):
        warns.add(f"{where}: 경로가 {{host}}/ 로 시작하지 않음: {url}")

    block = {
        "method": method,
        "path": path,
        "auth": auth,
        "body": compact_body(raw_body, where, warns),
        "status": status,
        "asserts": " ; ".join(asserts),
    }
    return block, k


def parse_file(path, warns):
    file_name = os.path.basename(path)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    blocks = []
    pending = []  # 요청 바로 위에 붙어 있는 연속 주석 줄
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if s == "":
            if pending:
                warns.add(f"{file_name}:{i + 1}: 주석이 빈 줄로 요청과 떨어져 제목에 연결되지 않음: {' / '.join(pending)}")
                pending = []
            i += 1
            continue
        if line.startswith("#"):
            pending.append(line[1:].strip())
            i += 1
            continue
        if METHOD_RE.match(s):
            block, nxt = parse_block(lines, i, file_name, warns)
            if block is None:
                pending = []
                i = nxt
                continue
            block["title"] = " / ".join(pending)
            if not block["title"]:
                warns.add(f"{file_name}:{i + 1}: 바로 위 주석이 없어 제목이 비어 있음 ({block['method']} {block['path']})")
            pending = []
            block["file"] = file_name
            block["index"] = len(blocks) + 1
            blocks.append(block)
            i = nxt
            continue
        warns.add(f"{file_name}:{i + 1}: 알 수 없는 최상위 라인 `{s}`")
        i += 1
    if pending:
        warns.add(f"{file_name}: 파일 끝의 주석이 어떤 요청에도 연결되지 않음: {' / '.join(pending)}")
    return blocks


def kind_of(title, previous_kind):
    # Setup·Cleanup 블록은 채점 대상이 아니다. 제목 없는 블록은 같은 파일의 바로 앞 블록과 같은 묶음으로 본다.
    lowered = title.lower()
    if lowered.startswith("setup"):
        return "setup"
    if lowered.startswith("cleanup"):
        return "cleanup"
    if title == "" and previous_kind is not None:
        return previous_kind
    return "behavior"


def to_row(block, previous_kind=None):
    stem = os.path.splitext(block["file"])[0]
    title = block["title"]
    kind = kind_of(title, previous_kind)
    return OrderedDict([
        ("id", f"{stem}-{block['index']:02d}"),
        ("file", block["file"]),
        ("title", title),
        ("kind", kind),
        ("method", block["method"]),
        ("path", block["path"]),
        ("auth", block["auth"]),
        ("body", block["body"]),
        ("status", block["status"]),
        ("asserts", block["asserts"]),
    ])


def write_csv(rows, out_path):
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_summary(rows, files, out_path, warns):
    total = len(rows)
    behavior = [r for r in rows if r["kind"] == "behavior"]
    setup_count = total - len(behavior)
    per_file = OrderedDict((f, 0) for f in files)
    for r in behavior:
        per_file[r["file"]] += 1
    per_status = Counter(r["status"] for r in behavior)

    lines = []
    lines.append("# RealWorld Hurl 기준 체크리스트 요약")
    lines.append("")
    lines.append(f"- 입력 파일 수: {len(files)}")
    lines.append(f"- 전체 요청 블록: {total}")
    lines.append(f"- behavior 블록: {len(behavior)}")
    lines.append(f"- setup 블록: {setup_count}")
    lines.append("")
    lines.append("## 파일별 behavior 블록 수")
    lines.append("")
    lines.append("| 파일 | behavior 수 |")
    lines.append("| --- | ---: |")
    for f, c in per_file.items():
        lines.append(f"| {f} | {c} |")
    lines.append(f"| **합계** | **{len(behavior)}** |")
    lines.append("")
    lines.append("## 상태 코드별 behavior 블록 수")
    lines.append("")
    lines.append("| HTTP 상태 | behavior 수 |")
    lines.append("| --- | ---: |")
    for code in sorted(per_status, key=lambda x: int(x) if x.isdigit() else 9999):
        lines.append(f"| {code} | {per_status[code]} |")
    lines.append(f"| **합계** | **{len(behavior)}** |")
    lines.append("")
    lines.append("## 파서 경고")
    lines.append("")
    if warns:
        for w in warns:
            lines.append(f"- {w}")
    else:
        lines.append("- 없음")
    lines.append("")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input-dir", default=DEFAULT_INPUT_DIR, help="Hurl 파일이 있는 디렉터리")
    ap.add_argument(
        "--output-dir",
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        help="ground-truth.csv와 ground-truth-summary.md를 쓸 디렉터리 (기본: 스크립트의 상위 디렉터리)",
    )
    args = ap.parse_args(argv)

    files = sorted(glob.glob(os.path.join(args.input_dir, "*.hurl")))
    if not files:
        print(f"Hurl 파일을 찾지 못함: {args.input_dir}", file=sys.stderr)
        return 1

    warns = Warnings()
    rows = []
    file_names = []
    for path in files:
        blocks = parse_file(path, warns)
        file_names.append(os.path.basename(path))
        previous_kind = None
        for b in blocks:
            row = to_row(b, previous_kind)
            previous_kind = row["kind"]
            rows.append(row)

    os.makedirs(args.output_dir, exist_ok=True)
    csv_path = os.path.join(args.output_dir, "ground-truth.csv")
    md_path = os.path.join(args.output_dir, "ground-truth-summary.md")
    write_csv(rows, csv_path)
    write_summary(rows, file_names, md_path, warns.items)

    behavior = sum(1 for r in rows if r["kind"] == "behavior")
    print(f"파일 {len(files)}개, 블록 {len(rows)}개 (behavior {behavior}, setup {len(rows) - behavior})")
    print(f"CSV: {csv_path}")
    print(f"요약: {md_path}")
    for w in warns.items:
        print(f"경고: {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
