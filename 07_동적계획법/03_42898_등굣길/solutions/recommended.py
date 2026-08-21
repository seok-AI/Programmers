"""행을 순회하며 왼쪽·위쪽 경로 수를 1차원 DP에 누적.

복잡도: O(m*n) time, O(m) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(m, n, puddles):
    # 이 구현의 선택: 행을 순회하며 왼쪽·위쪽 경로 수를 1차원 DP에 누적
    # 상태 정의: 현재 행에서 각 열까지 오는 경로 수를 1차원 DP에 누적한다.
    # 핵심 불변식: 열 j 처리 뒤 dp[j]는 위쪽 경로와 현재 행 왼쪽 경로의 합이며 물웅덩이면 0이다.
    blocked = {(column, row) for column, row in puddles}
    ways = [0] * (m + 1)
    ways[1] = 1
    for row in range(1, n + 1):
        for column in range(1, m + 1):
            if (column, row) in blocked:
                ways[column] = 0
            elif column > 1:
                ways[column] = (ways[column] + ways[column - 1]) % 1_000_000_007
    return ways[m]
