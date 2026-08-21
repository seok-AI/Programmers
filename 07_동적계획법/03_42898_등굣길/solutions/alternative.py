"""격자 모양 2차원 DP로 경로 수 계산.

복잡도: O(m*n) time, O(m*n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42898/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(m, n, puddles):
    # 이 구현의 선택: 격자 모양 2차원 DP로 경로 수 계산
    # 상태 정의: 현재 행에서 각 열까지 오는 경로 수를 1차원 DP에 누적한다.
    # 핵심 불변식: 열 j 처리 뒤 dp[j]는 위쪽 경로와 현재 행 왼쪽 경로의 합이며 물웅덩이면 0이다.
    blocked = {tuple(point) for point in puddles}
    ways = [[0] * (m + 1) for _ in range(n + 1)]
    ways[1][1] = 1
    for row in range(1, n + 1):
        for column in range(1, m + 1):
            if (column, row) in blocked:
                ways[row][column] = 0
            elif (column, row) != (1, 1):
                ways[row][column] = (ways[row - 1][column] + ways[row][column - 1]) % 1_000_000_007
    return ways[n][m]
