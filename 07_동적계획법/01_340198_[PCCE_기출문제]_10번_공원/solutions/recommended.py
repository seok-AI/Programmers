"""빈 칸으로 끝나는 최대 정사각형 DP 후 돗자리 선택.

복잡도: O(h*w + m log m) time, O(w) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(mats, park):
    # 이 구현의 선택: 빈 칸으로 끝나는 최대 정사각형 DP 후 돗자리 선택
    # 상태 정의: 현재 칸을 오른쪽 아래로 하는 연속 빈 정사각형의 최대 변 길이를 1차원 DP에 둔다.
    # 핵심 불변식: 빈 칸의 DP 값은 위·왼쪽·왼쪽 위 세 정사각형 최솟값에 1을 더한 값이다.
    width = len(park[0])
    previous = [0] * (width + 1)
    largest = 0
    for row in park:
        current = [0] * (width + 1)
        for column, value in enumerate(row, 1):
            if value == "-1":
                current[column] = 1 + min(
                    current[column - 1], previous[column], previous[column - 1]
                )
                largest = max(largest, current[column])
        previous = current
    possible = [size for size in mats if size <= largest]
    return max(possible, default=-1)
