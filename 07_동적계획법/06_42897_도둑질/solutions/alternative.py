"""첫 집을 고르는 경우와 버리는 경우의 DP 배열.

복잡도: O(n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42897/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(money):
    # 이 구현의 선택: 첫 집을 고르는 경우와 버리는 경우의 DP 배열
    # 상태 정의: 원형 배열을 첫 집 제외 구간과 마지막 집 제외 구간 두 선형 문제로 나눈다.
    # 핵심 불변식: 선형 구간의 각 위치 최적값은 이전 최적과 두 칸 전 최적+현재 돈 중 큰 값이다.
    if len(money) <= 3:
        return max(money)

    def table(values):
        dp = [0] * (len(values) + 1)
        dp[1] = values[0]
        for index in range(2, len(values) + 1):
            dp[index] = max(dp[index - 1], dp[index - 2] + values[index - 1])
        return dp[-1]

    return max(table(money[:-1]), table(money[1:]))
