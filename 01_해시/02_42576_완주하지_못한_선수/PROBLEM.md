# 완주하지 못한 선수 — 오프라인 문제 명세

> 이 문서는 공식 지문을 복제하지 않고, 인터넷 없이 풀이할 수 있도록 문제의
> 동작 규칙과 제한을 독립적으로 재서술한 명세입니다.

## 한눈에 보기

| 항목 | 내용 |
|---|---|
| 난이도 | Level 1 |
| 학습 유형 | 해시 |
| 호출 함수 | `solution(participant, completion)` |
| 매개변수 | `participant`, `completion` |
| 반환형 | `str` |

## 문제

마라톤 참가자 명단 `participant`와 완주자 명단 `completion`이 주어진다.
참가자 중 정확히 한 명만 완주 명단에 없다. 이름이 같은 참가자가 여러 명일 수
있으므로 등장 횟수까지 고려하여 완주하지 못한 한 사람의 이름을 반환하라.

## 함수 인터페이스

```python
def solution(participant, completion):
    ...
```

매개변수는 위 순서로 전달하며, 반환값은 문제에서 요구한 Python 값이어야 한다.
표준 입력을 읽거나 표준 출력에 답을 쓰는 문제가 아니다.

## 규칙과 제한사항

- `participant`의 길이는 1 이상 100,000 이하이다.
- `completion`의 길이는 `len(participant) - 1`이다.
- 이름은 길이 1~20의 알파벳 소문자 문자열이다.
- 서로 다른 참가자가 같은 이름을 사용할 수 있다.

## 공개 예제

> `INPUT`은 `solution()`에 전달되는 매개변수이며, `OUTPUT`은 함수가 반환해야 할
> 값입니다. 짧은 값은 좌우 표로, 긴 격자·중첩 배열은 코드 블록으로 표시합니다.

### 예제 1

| INPUT | OUTPUT |
|---|---|
| `participant = ['leo', 'kiki', 'eden']; completion = ['eden', 'kiki']` | `'leo'` |

### 예제 2

**INPUT**

```python
participant = ['marina', 'josipa', 'nikola', 'vinko', 'filipa']
completion = ['josipa', 'filipa', 'marina', 'nikola']
```

**OUTPUT**

```python
'vinko'
```

### 예제 3

| INPUT | OUTPUT |
|---|---|
| `participant = ['mislav', 'stanko', 'mislav', 'ana']; completion = ['stanko', 'ana', 'mislav']` | `'mislav'` |

## 예제 해설

> **핵심:** 첫 예제에서는 완주자 이름의 등장 횟수를 참가자 명단에서 빼면 `leo`만 한 번 남으므로 이를 반환한다.

---

## 출처

- 프로그래머스 문제 번호: 42576
- 공식 페이지(온라인 확인용): <https://school.programmers.co.kr/learn/courses/30/lessons/42576>
