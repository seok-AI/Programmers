# 최소직사각형

- 구분: 고득점 Kit
- 난이도: Level 1
- 유형: 완전탐색
- 오프라인 문제 명세: [PROBLEM.md](./PROBLEM.md)
- 주석 포함 예시 풀이: [solutions/README.md](./solutions/README.md)
- 공식 문제: <https://school.programmers.co.kr/learn/courses/30/lessons/86491>
- 함수: `solution(sizes)`
- 포함된 테스트: 공식 공개 예제 3개 + 자체 경계 사례 2개

## 풀이 방법

1. 이 폴더의 `PROBLEM.md`에서 문제 규칙, 제한사항, 예제를 읽습니다.
2. `solution.py`의 `solution()` 함수를 구현합니다.
3. 저장한 뒤 저장소 루트에서 아래 명령을 실행합니다.
4. 통과 후 `solutions/README.md`와 두 예시 답안을 비교하며 복기합니다.

```bash
python3 tools/judge.py "05_완전탐색/03_86491_최소직사각형"
```

채점기는 `sizes` 순서로 함수를 호출합니다. `tests.json`은 공개 예제,
`edge_tests.json`은 자체 경계 사례입니다. 제출 전에는 자신이 찾은 반례도
`edge_tests.json`에 더 추가하세요.


## `solution.py` 직접 디버깅

아래처럼 파일을 직접 실행하면 두 테스트 파일의 모든 입력, 기대값, 실제 반환값,
실행 시간과 예외 traceback이 출력됩니다.

```bash
python3 "05_완전탐색/03_86491_최소직사각형/solution.py"
```
