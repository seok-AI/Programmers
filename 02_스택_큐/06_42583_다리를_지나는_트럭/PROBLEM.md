# 다리를 지나는 트럭 — 오프라인 문제 명세

> 이 문서는 공식 지문을 복제하지 않고, 인터넷 없이 풀이할 수 있도록 문제의
> 동작 규칙과 제한을 독립적으로 재서술한 명세입니다.

## 한눈에 보기

| 항목 | 내용 |
|---|---|
| 난이도 | Level 2 |
| 학습 유형 | 스택/큐 |
| 호출 함수 | `solution(bridge_length, weight, truck_weights)` |
| 매개변수 | `bridge_length`, `weight`, `truck_weights` |
| 반환형 | `int` |

## 문제

트럭은 `truck_weights`의 순서대로 길이 `bridge_length`인 일차선
다리를 건넌다. 한 칸 이동에 1초가 걸리며, 다리 위 트럭 무게 합은 `weight`를
넘을 수 없다. 대기 시간을 포함하여 모든 트럭이 다리에서 완전히 내려오는
최소 시각을 반환하라.

## 함수 인터페이스

```python
def solution(bridge_length, weight, truck_weights):
    ...
```

매개변수는 위 순서로 전달하며, 반환값은 문제에서 요구한 Python 값이어야 한다.
표준 입력을 읽거나 표준 출력에 답을 쓰는 문제가 아니다.

## 규칙과 제한사항

- `bridge_length`와 `weight`는 각각 1 이상 10,000 이하이다.
- 트럭 수는 1 이상 10,000 이하이다.
- 각 트럭 무게는 1 이상 `weight` 이하이다.
- 다리에는 동시에 최대 `bridge_length`대가 있을 수 있다.

## 공개 예제

> `INPUT`은 `solution()`에 전달되는 매개변수이며, `OUTPUT`은 함수가 반환해야 할
> 값입니다. 짧은 값은 좌우 표로, 긴 격자·중첩 배열은 코드 블록으로 표시합니다.

### 예제 1

| INPUT | OUTPUT |
|---|---|
| `bridge_length = 2; weight = 10; truck_weights = [7, 4, 5, 6]` | `8` |

### 예제 2

| INPUT | OUTPUT |
|---|---|
| `bridge_length = 100; weight = 100; truck_weights = [10]` | `101` |

### 예제 3

| INPUT | OUTPUT |
|---|---|
| `bridge_length = 100; weight = 100; truck_weights = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]` | `110` |

## 예제 해설

> **핵심:** 첫 예제는 다리 길이와 무게 제한 때문에 트럭 진입 시각이 달라진다. 각 트럭의 진입·퇴장 시각을 함께 추적하면 마지막 트럭이 8초에 내려온다.

---

## 출처

- 프로그래머스 문제 번호: 42583
- 공식 페이지(온라인 확인용): <https://school.programmers.co.kr/learn/courses/30/lessons/42583>
