"""필요 개수 집합을 재귀적으로 조합해 메모이제이션.

복잡도: O(8^3*S^2) worst time, O(8*S) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42895/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from functools import lru_cache

def solution(N, number):
    # 이 구현의 선택: 필요 개수 집합을 재귀적으로 조합해 메모이제이션
    # 상태 정의: dp[i]를 N을 정확히 i번 사용해 만들 수 있는 모든 수의 집합으로 둔다.
    # 핵심 불변식: dp[i]에는 이어 붙인 수와 dp[j], dp[i-j]의 사칙연산 결과가 모두 들어간다.
    @lru_cache(None)
    def values(count):
        result = {int(str(N) * count)}
        for left_count in range(1, count):
            for left in values(left_count):
                for right in values(count - left_count):
                    result |= {left + right, left - right, left * right}
                    if right:
                        result.add(left // right)
        return result

    for count in range(1, 9):
        if number in values(count):
            return count
    return -1
