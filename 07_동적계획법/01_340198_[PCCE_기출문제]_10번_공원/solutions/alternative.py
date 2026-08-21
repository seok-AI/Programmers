"""2차원 누적합으로 큰 돗자리부터 빈 영역 탐색.

복잡도: O(h*w + m*h*w) time, O(h*w) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/340198/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(mats, park):
    # 이 구현의 선택: 2차원 누적합으로 큰 돗자리부터 빈 영역 탐색
    # 상태 정의: 현재 칸을 오른쪽 아래로 하는 연속 빈 정사각형의 최대 변 길이를 1차원 DP에 둔다.
    # 핵심 불변식: 빈 칸의 DP 값은 위·왼쪽·왼쪽 위 세 정사각형 최솟값에 1을 더한 값이다.
    height, width = len(park), len(park[0])
    occupied = [[0] * (width + 1) for _ in range(height + 1)]
    for row in range(height):
        for column in range(width):
            occupied[row + 1][column + 1] = (
                occupied[row][column + 1]
                + occupied[row + 1][column]
                - occupied[row][column]
                + (park[row][column] != "-1")
            )
    for size in sorted(mats, reverse=True):
        for bottom in range(size, height + 1):
            for right in range(size, width + 1):
                people = (
                    occupied[bottom][right]
                    - occupied[bottom - size][right]
                    - occupied[bottom][right - size]
                    + occupied[bottom - size][right - size]
                )
                if people == 0:
                    return size
    return -1
