#!/usr/bin/env python3
"""재현 가능한 2시간 3문제 모의고사 세션을 만들고 채점한다."""

from __future__ import annotations

import argparse
import json
import random
import re
from datetime import datetime, timedelta
from pathlib import Path

try:
    from .judge import ROOT, discover, run_problem
    from .progress import is_attempted
except ImportError:
    from judge import ROOT, discover, run_problem
    from progress import is_attempted


PRACTICE_DIR = ROOT / ".practice"
CURRENT = PRACTICE_DIR / "current_mock.json"


def level_of(directory: Path) -> int:
    readme = (directory / "README.md").read_text(encoding="utf-8")
    match = re.search(r"^- 난이도: Level (\d+)", readme, flags=re.MULTILINE)
    return int(match.group(1)) if match else 2


def load_current() -> tuple[Path, dict[str, object]]:
    if not CURRENT.is_file():
        raise ValueError("진행 중인 모의고사가 없습니다. 먼저 start를 실행하세요.")
    pointer = json.loads(CURRENT.read_text(encoding="utf-8"))
    session_path = PRACTICE_DIR / str(pointer["session"])
    if not session_path.is_file():
        raise ValueError(f"세션 파일을 찾지 못했습니다: {session_path}")
    return session_path, json.loads(session_path.read_text(encoding="utf-8"))


def choose_problems(levels: list[int], seed: int, include_solved: bool) -> list[Path]:
    candidates = [
        path
        for path in discover()
        if include_solved or not is_attempted(path / "solution.py")
    ]
    randomizer = random.Random(seed)
    randomizer.shuffle(candidates)
    selected: list[Path] = []
    used_categories: set[str] = set()
    for level in levels:
        pool = [
            path
            for path in candidates
            if path not in selected
            and level_of(path) == level
            and path.parent.name not in used_categories
        ]
        if not pool:
            pool = [
                path for path in candidates if path not in selected and level_of(path) == level
            ]
        if not pool:
            raise ValueError(
                f"Level {level} 미시도 문제가 부족합니다. --include-solved 또는 다른 --levels를 사용하세요."
            )
        choice = pool[0]
        selected.append(choice)
        used_categories.add(choice.parent.name)
    return selected


def show_session(session: dict[str, object]) -> None:
    started = datetime.fromisoformat(str(session["started_at"]))
    deadline = datetime.fromisoformat(str(session["deadline"]))
    now = datetime.now().astimezone()
    remaining = deadline - now
    if session.get("finished_at"):
        timing = f"종료됨: {session['finished_at']}"
    elif remaining.total_seconds() > 0:
        minutes, seconds = divmod(int(remaining.total_seconds()), 60)
        timing = f"남은 시간: {minutes}분 {seconds}초"
    else:
        timing = f"제한 시간 초과: {int(-remaining.total_seconds() // 60)}분 경과"
    print(f"시작: {started.isoformat(timespec='seconds')}")
    print(f"마감: {deadline.isoformat(timespec='seconds')} / {timing}")
    print(f"seed: {session['seed']}")
    for index, raw in enumerate(session["problems"], start=1):
        print(f"{index}. {raw}")


def start(args: argparse.Namespace) -> int:
    if CURRENT.is_file():
        try:
            _, current = load_current()
            if not current.get("finished_at"):
                raise ValueError("끝내지 않은 세션이 있습니다. finish로 채점한 뒤 새로 시작하세요.")
        except (OSError, json.JSONDecodeError, KeyError):
            raise ValueError("현재 세션 포인터가 손상되었습니다. 파일을 확인하세요.")

    levels = [int(value) for value in args.levels.split(",") if value.strip()]
    if not levels or any(level not in (1, 2, 3) for level in levels):
        raise ValueError("--levels는 1,2,2처럼 Level 1~3을 쉼표로 지정하세요.")
    seed = args.seed if args.seed is not None else int(datetime.now().strftime("%Y%m%d"))
    selected = choose_problems(levels, seed, args.include_solved)
    now = datetime.now().astimezone()
    session = {
        "seed": seed,
        "minutes": args.minutes,
        "started_at": now.isoformat(),
        "deadline": (now + timedelta(minutes=args.minutes)).isoformat(),
        "problems": [str(path.relative_to(ROOT)) for path in selected],
        "finished_at": None,
        "score": None,
    }
    PRACTICE_DIR.mkdir(exist_ok=True)
    filename = f"mock_{now.strftime('%Y%m%d_%H%M%S')}.json"
    session_path = PRACTICE_DIR / filename
    session_path.write_text(json.dumps(session, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    CURRENT.write_text(json.dumps({"session": filename}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("모의고사를 시작했습니다. 지금부터 PROBLEM.md만 읽고 풀이하세요.")
    show_session(session)
    print("\n완료 후: python3 tools/mock.py finish")
    return 0


def status(_: argparse.Namespace) -> int:
    _, session = load_current()
    show_session(session)
    return 0


def finish(args: argparse.Namespace) -> int:
    session_path, session = load_current()
    if session.get("finished_at"):
        raise ValueError("이미 종료한 세션입니다.")
    total_passed = total_failed = solved = 0
    for raw in session["problems"]:
        directory = ROOT / str(raw)
        passed, failed = run_problem(directory, args.timeout)
        total_passed += passed
        total_failed += failed
        solved += failed == 0
    now = datetime.now().astimezone()
    session["finished_at"] = now.isoformat()
    session["score"] = {
        "solved_problems": solved,
        "total_problems": len(session["problems"]),
        "passed_cases": total_passed,
        "failed_cases": total_failed,
        "within_time": now <= datetime.fromisoformat(str(session["deadline"])),
    }
    session_path.write_text(json.dumps(session, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"\n모의고사 종료: {solved}/{len(session['problems'])}문제, "
        f"테스트 {total_passed}개 통과 / {total_failed}개 실패, "
        f"제한 시간 {'준수' if session['score']['within_time'] else '초과'}"
    )
    print(f"기록: {session_path.relative_to(ROOT)}")
    return 0 if total_failed == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="시간 제한 모의고사 세션")
    commands = parser.add_subparsers(dest="command", required=True)
    start_parser = commands.add_parser("start", help="새 세션 선택·타이머 시작")
    start_parser.add_argument("--minutes", type=int, default=120)
    start_parser.add_argument("--levels", default="1,2,2", help="기본: 1,2,2")
    start_parser.add_argument("--seed", type=int, help="같은 문제 구성을 재현할 정수")
    start_parser.add_argument("--include-solved", action="store_true")
    start_parser.set_defaults(handler=start)
    status_parser = commands.add_parser("status", help="현재 문제와 남은 시간 확인")
    status_parser.set_defaults(handler=status)
    finish_parser = commands.add_parser("finish", help="선택된 solution.py 채점·기록")
    finish_parser.add_argument("--timeout", type=float, default=2.0)
    finish_parser.set_defaults(handler=finish)
    args = parser.parse_args()
    if getattr(args, "minutes", 1) <= 0 or getattr(args, "timeout", 1) <= 0:
        parser.error("시간은 0보다 커야 합니다.")
    try:
        return args.handler(args)
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
