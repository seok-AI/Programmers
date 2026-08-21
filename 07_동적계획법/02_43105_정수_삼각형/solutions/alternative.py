"""꼭대기에서 각 칸까지 최대 합을 한 행씩 갱신.

복잡도: O(n^2) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/43105/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

import math

def solution(triangle):
    # 이 구현의 선택: 꼭대기에서 각 칸까지 최대 합을 한 행씩 갱신
    # 상태 정의: 각 칸에서 바닥까지 내려가 얻을 수 있는 최대 합을 저장한다.
    # 핵심 불변식: 아래 행의 값이 이미 최적이면 현재 칸은 두 자식 중 큰 값만 더하면 최적이다.
    previous = [triangle[0][0]]
    for row in triangle[1:]:
        current = [0] * len(row)
        for column, value in enumerate(row):
            left_parent = previous[column - 1] if column > 0 else -math.inf
            right_parent = previous[column] if column < len(previous) else -math.inf
            current[column] = value + max(left_parent, right_parent)
        previous = current
    return max(previous)
