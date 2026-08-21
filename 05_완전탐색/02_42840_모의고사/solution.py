"""프로그래머스 모의고사 풀이."""


def solution(answers):
    # TODO: 여기에 풀이를 작성하세요.
    pass

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
