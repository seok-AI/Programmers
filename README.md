# 프로그래머스 알고리즘 고득점 Kit — 로컬 연습 환경

프로그래머스 **고득점 Kit 47문제**와 각 유형별 **추가 Level 1 문제
1개씩(10문제)**, 총 57문제를 Python으로 바로 풀 수 있게 구성한 저장소입니다.

공식 Kit의 현재 유형과 문제 목록은 [프로그래머스 고득점 Kit][kit]를 기준으로
했습니다. 각 문제 폴더의 `PROBLEM.md`에는 문제의 동작 규칙, 매개변수,
반환값, 수치 제한과 공개 예제를 독립적으로 재서술해 두었습니다. 문제를 읽고
풀이하고 테스트하는 과정에는 인터넷 연결이 필요하지 않습니다.

알고리즘을 체계적으로 마스터하려면 [전체 훈련 로드맵](./MASTER_ROADMAP.md)부터
읽으세요. 각 유형 폴더의 `MASTERY_GUIDE.md`에는 유형 판별법, 핵심 사고방식,
구현 패턴, 추천 문제 순서와 오답 복기법이 있습니다.
진행 상황은 [훈련 기록 템플릿](./STUDY_LOG_TEMPLATE.md)으로 측정할 수 있습니다.

[kit]: https://school.programmers.co.kr/learn/challenges?tab=algorithm_practice_kit

## 빠른 시작

Python 3.10 이상만 있으면 별도 설치 없이 실행할 수 있습니다.

```bash
# 문제 목록
python3 tools/judge.py --list

# 문제 ID로 공개 예제와 경계 테스트 실행
python3 tools/judge.py 42576

# solution.py를 직접 실행해 입력·기대값·실제값·실행시간 확인
python3 "01_해시/02_42576_완주하지_못한_선수/solution.py"

# 폴더 경로로 실행
python3 tools/judge.py "01_해시/02_42576_완주하지_못한_선수"

# 전체 실행
python3 tools/judge.py --all

# 폴더와 테스트 데이터가 온전한지 검사
python3 tools/validate.py

# 유형 README의 문제 링크를 추천 학습 순서로 다시 생성
python3 tools/build_workspace.py --refresh-navigation

# 모든 권장/대안 예시 풀이를 공개 예제와 경계 테스트로 검증
python3 tools/check_example_solutions.py

# 한 문제의 사용자 풀이에 결정적 랜덤 입력 500개 교차검증
python3 tools/fuzz.py 42746

# 57문제의 랜덤 생성기와 두 예시 풀이를 문제당 500개씩 검증
python3 tools/fuzz.py --all --oracles-only

# 시간복잡도 퇴행이 컸던 문제의 최대·적대 입력 검사
python3 tools/stress.py --all

# 현재 solution.py 기준 유형별 진척 집계
python3 tools/progress.py --details

# 120분, Level 1·2·2 세 문제 모의고사 시작/현황/채점
python3 tools/mock.py start
python3 tools/mock.py status
python3 tools/mock.py finish

# 기본 57문제 밖의 오프라인 문제 추가
# 먼저 templates/new_problem_spec.json을 복사해 내용을 채우세요.
python3 tools/new_problem.py my_problem.json

# 시험 전에 손으로 재현할 최소 참조 구현 자체 검증
python3 snippets/bfs.py
python3 snippets/union_find.py
python3 snippets/dijkstra.py
```

처음에는 모든 `solution.py`가 빈 템플릿이므로 테스트 실패가 정상입니다.
문제 폴더의 `solution.py`만 수정하면 됩니다. 테스트를 추가하려면 같은 폴더의
`edge_tests.json`에 `name`, `args`, `expected` 형식으로 사례를 추가하세요.
각 `solution.py`를 직접 실행하면 고정 사례의 매개변수별 입력, 기대값, 실제 반환값,
실행시간, 함수가 출력한 내용과 예외 traceback을 볼 수 있습니다. 이어서 결정적 랜덤
입력 500개를 두 예시 풀이와 교차검증하며, 랜덤 사례는 실패 입력만 자세히 출력합니다.
프로그래머스에는 `solution()` 함수 부분만 제출하세요. 테스트가 증명할 수 있는 범위와
한계는 [테스트 전략](./TESTING_STRATEGY.md)에 정리했습니다.

각 문제 폴더는 다음 파일로 구성됩니다.

- `PROBLEM.md`: 오프라인 문제 설명, 전체 규칙·제한사항, 공개 예제
- `solution.py`: 프로그래머스와 같은 `solution(...)` 풀이 템플릿
- `tests.json`: 출처를 구분해 보존하는 공식 공개 예제
- `edge_tests.json`: 최소값·동률·불가능·함정 조건을 담은 자체 경계 테스트
- `HINTS.md`: 복잡도→접근→불변식→의사코드 순서로 여는 단계별 힌트
- `README.md`: 유형 정보와 실행 명령
- `solutions/recommended.py`: 최대 제한을 고려한 주석 포함 권장 풀이
- `solutions/alternative.py`: 온라인 공개 풀이의 널리 쓰이는 접근을 독립 재작성한 주석 포함 풀이
- `solutions/README.md`: 풀이 비교, 복잡도, 문제별 인터넷 참고 링크
- `solutions/SOURCES.md`: 고정된 공개 스냅숏, 확인일과 독립 재작성 범위

문제 폴더 이름의 첫 두 자리는 각 `MASTERY_GUIDE.md`가 권장하는 학습 순서입니다.
예를 들어 `04_정렬/01_12915_...`에서 `01`은 정렬 유형의 첫 학습 문제이고,
`12915`는 프로그래머스 문제 번호입니다.

먼저 `solution.py`로 직접 푼 뒤 `solutions/`를 확인하세요. 예시 코드는 공개적으로
널리 쓰이는 알고리즘 접근을 참고해 이 저장소용으로 독립 작성했으며, 출처를 추적할
수 있도록 각 문제의 공식 풀이 Q&A와 공개 풀이 모음 링크를 함께 기록했습니다.
`recommended`는 제한을 고려한 표준 사고 흐름을 뜻하며 특정 PC의 단일 입력에서
항상 가장 빠르다는 뜻은 아닙니다. 두 예시 파일은 현재 최대 제한에 맞는 복잡도로
구성하고, 작은 입력에서만 유효한 완전탐색은 풀이 설명의 반례로만 다룹니다.

## 유형 구성

| 폴더 | 유형 | Kit | 추가 | 합계 |
|---|---|---:|---:|---:|
| `01_해시` | 해시 | 5 | 1 | 6 |
| `02_스택_큐` | 스택/큐 | 6 | 1 | 7 |
| `03_힙` | 힙 | 3 | 1 | 4 |
| `04_정렬` | 정렬 | 3 | 1 | 4 |
| `05_완전탐색` | 완전탐색 | 7 | 1 | 8 |
| `06_탐욕법` | 탐욕법 | 6 | 1 | 7 |
| `07_동적계획법` | 동적계획법 | 5 | 1 | 6 |
| `08_DFS_BFS` | DFS/BFS | 7 | 1 | 8 |
| `09_이분탐색` | 이분탐색 | 2 | 1 | 3 |
| `10_그래프` | 그래프 | 3 | 1 | 4 |
| **합계** |  | **47** | **10** | **57** |

## 추가 Level 1 분류 원칙

추가 문제는 프로그래머스의 공식 Kit 소속이 아니라, 각 기법을 낮은 난이도에서
연습하기 위해 학습 관점으로 재분류한 문제입니다. Level 1 특성상 더 단순한
풀이도 가능한 문제가 있으며, 각 문제 README에 해당 유형으로 고른 이유를
적었습니다. `공원`, `공원 산책`, `예산`, `키패드 누르기`는 대표 유형 문제가
아니라는 경고와 먼저 풀어야 할 핵심 문제도 함께 표시했습니다.

## 로컬 채점 범위

- 프로그래머스처럼 `solution(...)` 함수를 직접 호출합니다.
- 테스트마다 입력을 깊은 복사해 이전 테스트의 변경이 다음 테스트에 번지지 않습니다.
- 기본 시간 제한은 사례당 2초이며 `--timeout`으로 바꿀 수 있습니다.
- 공개 예제 114개와 자체 경계 테스트 114개를 분리해 실행합니다.
- `tools/stress.py`는 큰 입력 위험이 있는 22문제의 권장·대안 풀이 44개를
  최대·적대 입력으로 검사합니다.
- `tools/fuzz.py`는 기본 57문제 모두에서 문제당 500개의 작은 명세 내 입력을 만들고,
  권장·대안 풀이가 합의한 값과 사용자 풀이를 비교합니다.
- 로컬 테스트 통과는 실제 제출 통과를 보장하지 않습니다. 공식 비공개 테스트와 정확한
  제한사항은 공식 사이트에서 확인해야 합니다.

`python3 tools/build_workspace.py`의 기본 실행은 네트워크에 접속하거나 파일을
바꾸지 않습니다. 공식 공개 예제를 다시 받아야 할 때만
`python3 tools/build_workspace.py --refresh-public-examples`를 실행하고 확인 질문에
동의하세요. 기존 `solution.py`와 `edge_tests.json`은 보존하며, README·오프라인
명세·공개 예제는 갱신합니다. 오프라인 명세만 다시 만들려면 `make specs`를 사용합니다.

## Git으로 재풀이 이력 남기기

파일 탐색기의 `U`는 Git의 **untracked**, 즉 아직 첫 커밋에 포함되지 않은 파일이라는
뜻입니다. 원격 저장소 연결 여부와는 관계없습니다. 이 저장소는 사용자의 이름·이메일과
커밋 정책을 임의로 정할 수 없어 자동 커밋하지 않습니다.

첫 기준점을 직접 남긴 뒤 문제 풀이와 재풀이를 작은 커밋으로 분리하면 D+1/D+7의
변화를 실제 코드로 비교할 수 있습니다.

```bash
git add -A
git commit -m "chore: initialize offline coding-test workspace"

# 예시: 첫 풀이와 재풀이를 별도 기록
git add "04_정렬/04_42746_가장_큰_수/solution.py"
git commit -m "solve(sort): 42746 first pass"
git commit -am "review(sort): 42746 D+1 without hints"
```

`tools/progress.py`는 현재 테스트 통과 여부를 자동 집계하지만 날짜별 재현율은 Git
커밋이나 `STUDY_LOG_TEMPLATE.md`의 기록이 있어야 측정할 수 있습니다. 모의고사 세션은
`.practice/`에 보존되며 개인 실행 기록이라 Git에서는 제외됩니다.
