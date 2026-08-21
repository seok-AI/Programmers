# 단어 변환 — 오프라인 문제 명세

> 이 문서는 공식 지문을 복제하지 않고, 인터넷 없이 풀이할 수 있도록 문제의
> 동작 규칙과 제한을 독립적으로 재서술한 명세입니다.

## 한눈에 보기

| 항목 | 내용 |
|---|---|
| 난이도 | Level 3 |
| 학습 유형 | 깊이/너비 우선 탐색(DFS/BFS) |
| 호출 함수 | `solution(begin, target, words)` |
| 매개변수 | `begin`, `target`, `words` |
| 반환형 | `int` |

## 문제

`begin`에서 시작하여 한 단계마다 알파벳 한 글자만 바꾸되,
바꾼 결과는 반드시 `words` 안의 단어여야 한다. `target`까지 필요한 최소
단계 수를 반환하고 변환이 불가능하면 0을 반환하라.

## 함수 인터페이스

```python
def solution(begin, target, words):
    ...
```

매개변수는 위 순서로 전달하며, 반환값은 문제에서 요구한 Python 값이어야 한다.
표준 입력을 읽거나 표준 출력에 답을 쓰는 문제가 아니다.

## 규칙과 제한사항

- 모든 단어는 길이 3~10의 알파벳 소문자 문자열이고 길이가 같다.
- `words`에는 중복 없는 단어가 3개 이상 50개 이하 있다.
- `begin`과 `target`은 서로 다르다.

## 공개 예제

> `INPUT`은 `solution()`에 전달되는 매개변수이며, `OUTPUT`은 함수가 반환해야 할
> 값입니다. 짧은 값은 좌우 표로, 긴 격자·중첩 배열은 코드 블록으로 표시합니다.

### 예제 1

| INPUT | OUTPUT |
|---|---|
| `begin = 'hit'; target = 'cog'; words = ['hot', 'dot', 'dog', 'lot', 'log', 'cog']` | `4` |

### 예제 2

| INPUT | OUTPUT |
|---|---|
| `begin = 'hit'; target = 'cog'; words = ['hot', 'dot', 'dog', 'lot', 'log']` | `0` |

## 예제 해설

> **핵심:** 한 글자만 다른 단어로 이동하는 그래프에서 `hit→hot→dot→dog→cog`가 네 번의 변환으로 목표에 도달한다.

---

## 출처

- 프로그래머스 문제 번호: 43163
- 공식 페이지(온라인 확인용): <https://school.programmers.co.kr/learn/courses/30/lessons/43163>
