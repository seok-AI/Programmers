"""구간의 최솟값·최댓값을 재귀 메모이제이션.

복잡도: O(n^3) time, O(n^2) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/1843/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from functools import lru_cache
import math

def solution(arr):
    # 이 구현의 선택: 구간의 최솟값·최댓값을 재귀 메모이제이션
    # 상태 정의: min[i][j], max[i][j]를 i번째 수부터 j번째 수까지 식의 최소·최대값으로 둔다.
    # 핵심 불변식: 모든 분할 위치와 양쪽 극값 조합을 보면 뺄셈에서 필요한 반대 극값까지 빠짐없이 포함된다.
    numbers = tuple(map(int, arr[::2]))
    operators = arr[1::2]

    @lru_cache(None)
    def bounds(left, right):
        if left == right:
            return numbers[left], numbers[left]
        low, high = math.inf, -math.inf
        for split in range(left, right):
            left_low, left_high = bounds(left, split)
            right_low, right_high = bounds(split + 1, right)
            if operators[split] == "+":
                values = (left_low + right_low, left_high + right_high)
            else:
                values = (left_low - right_high, left_high - right_low)
            low, high = min(low, *values), max(high, *values)
        return low, high

    return bounds(0, len(numbers) - 1)[1]
