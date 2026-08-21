#!/usr/bin/env python3
"""기존 풀이 본문을 보존하면서 모든 solution.py에 직접 실행 블록을 설치한다."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKER = "# LOCAL_TEST_RUNNER"
RUNNER_BLOCK = r'''


# LOCAL_TEST_RUNNER: 이 아래는 로컬 실행용이며 solution 함수 제출 코드와 분리되어 있습니다.
if __name__ == "__main__":
    import sys as _sys
    from pathlib import Path as _Path

    _tests_path = _Path(__file__).with_name("tests.json")
    if _tests_path.is_file():
        _workspace_root = _Path(__file__).resolve().parents[2]
        if str(_workspace_root) not in _sys.path:
            _sys.path.insert(0, str(_workspace_root))
        from tools.direct_runner import run_local_tests as _run_local_tests

        raise SystemExit(_run_local_tests(solution, _tests_path))
'''


def main() -> int:
    sources = sorted(ROOT.glob("[0-9][0-9]_*/**/solution.py"))
    changed = 0
    documented = 0
    for source in sources:
        current = source.read_text(encoding="utf-8")
        if MARKER not in current:
            source.write_text(current.rstrip() + RUNNER_BLOCK + "\n", encoding="utf-8")
            changed += 1

        readme_path = source.with_name("README.md")
        readme = readme_path.read_text(encoding="utf-8")
        heading = "## `solution.py` 직접 디버깅"
        if heading not in readme:
            relative = source.relative_to(ROOT)
            readme += f"""

{heading}

아래처럼 파일을 직접 실행하면 `tests.json`의 모든 입력, 기대값, 실제 반환값,
실행 시간과 예외 traceback이 출력됩니다.

```bash
python3 "{relative}"
```
"""
            readme_path.write_text(readme, encoding="utf-8")
            documented += 1
    print(
        f"직접 실행 블록 설치: {changed}개 변경 / {len(sources)}개 확인, "
        f"README {documented}개 갱신"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
