# 아이템 줍기 — 오프라인 문제 명세

> 이 문서는 공식 지문을 복제하지 않고, 인터넷 없이 풀이할 수 있도록 문제의
> 동작 규칙과 제한을 독립적으로 재서술한 명세입니다.

## 한눈에 보기

| 항목 | 내용 |
|---|---|
| 난이도 | Level 3 |
| 학습 유형 | 깊이/너비 우선 탐색(DFS/BFS) |
| 호출 함수 | `solution(rectangle, characterX, characterY, itemX, itemY)` |
| 매개변수 | `rectangle`, `characterX`, `characterY`, `itemX`, `itemY` |
| 반환형 | `int` |

## 문제

`rectangle`에 주어진 축과 평행한 직사각형들의 합집합이 하나의 지형을 만든다.
캐릭터는 합집합의 가장 바깥 테두리만 따라 상하좌우로 이동한다. 시작 좌표
`(characterX, characterY)`에서 `(itemX, itemY)`까지의 최단 거리를
반환하라. 겹침으로 생긴 내부 선이나 내부 구멍의 경계는 이동 경로가 아니다.

## 함수 인터페이스

```python
def solution(rectangle, characterX, characterY, itemX, itemY):
    ...
```

매개변수는 위 순서로 전달하며, 반환값은 문제에서 요구한 Python 값이어야 한다.
표준 입력을 읽거나 표준 출력에 답을 쓰는 문제가 아니다.

## 규칙과 제한사항

- `rectangle`에는 1개 이상 4개 이하의 직사각형이 있다.
- 각 원소는 `[왼쪽 아래 x, 왼쪽 아래 y, 오른쪽 위 x, 오른쪽 위 y]`이다.
- 모든 좌표는 1 이상 50 이하의 정수이다.
- 서로 다른 직사각형은 x좌표나 y좌표를 공유하지 않아 꼭짓점/변만 맞닿지 않는다.
- 합집합은 분리되지 않고 한 직사각형이 다른 것에 완전히 포함되지 않는다.
- 시작과 아이템은 서로 다른 바깥 테두리 위 점이다.

## 공개 예제

> `INPUT`은 `solution()`에 전달되는 매개변수이며, `OUTPUT`은 함수가 반환해야 할
> 값입니다. 짧은 값은 좌우 표로, 긴 격자·중첩 배열은 코드 블록으로 표시합니다.

### 예제 1

**INPUT**

```python
rectangle = [[1, 1, 7, 4],
             [3, 2, 5, 5],
             [4, 3, 6, 9],
             [2, 6, 8, 8]]
characterX = 1
characterY = 3
itemX = 7
itemY = 8
```

**OUTPUT**

```python
17
```

### 예제 2

**INPUT**

```python
rectangle = [[1, 1, 8, 4],
             [2, 2, 4, 9],
             [3, 6, 9, 8],
             [6, 3, 7, 7]]
characterX = 9
characterY = 7
itemX = 6
itemY = 1
```

**OUTPUT**

```python
11
```

### 예제 3

| INPUT | OUTPUT |
|---|---|
| `rectangle = [[1, 1, 5, 7]]; characterX = 1; characterY = 1; itemX = 4; itemY = 7` | `9` |

### 예제 4

| INPUT | OUTPUT |
|---|---|
| `rectangle = [[2, 1, 7, 5], [6, 4, 10, 10]]; characterX = 3; characterY = 1; itemX = 7; itemY = 10` | `15` |

### 예제 5

| INPUT | OUTPUT |
|---|---|
| `rectangle = [[2, 2, 5, 5], [1, 3, 6, 4], [3, 1, 4, 6]]; characterX = 1; characterY = 4; itemX = 6; itemY = 3` | `10` |

## 예제 해설

> **핵심:** 겹친 직사각형의 내부를 제외한 바깥 테두리만 따라 이동한다. 좌표를 두 배로 확대해 모서리 지름길을 막고 최단거리를 구하면 17이다.

### 모델링 스케치 — 예제 1

```text
원래 좌표의 한 칸 이동       좌표를 2배로 확대한 뒤
(x, y) ── (x+1, y)    →    (2x, 2y) ─ 중간점 ─ (2x+2, 2y)

1. 직사각형들의 채워진 내부는 이동 금지로 표시한다.
2. 내부가 아닌 합성 도형의 바깥 테두리만 BFS 통로로 남긴다.
3. 확대 격자에서 얻은 최단거리 34를 2로 나누면 원래 거리 17이다.
```

두 배 확대는 대각선으로 닿은 서로 다른 테두리 사이에 중간점을 만들어, 실제로
연결되지 않은 모서리를 건너는 오류를 막는다.

---

## 출처

- 프로그래머스 문제 번호: 87694
- 공식 페이지(온라인 확인용): <https://school.programmers.co.kr/learn/courses/30/lessons/87694>
