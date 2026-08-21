"""명령마다 경로 전체의 경계와 장애물을 확인한 뒤 이동.

복잡도: O(routes*distance) time, O(1) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(park, routes):
    # 이 구현의 선택: 명령마다 경로 전체의 경계와 장애물을 확인한 뒤 이동
    # 상태 정의: 현재 로봇 좌표를 두고 명령 하나의 모든 중간 칸을 임시 검사한다.
    # 핵심 불변식: 명령이 끝까지 유효할 때만 현재 좌표가 목적지로 바뀌며, 하나라도 막히면 원위치이다.
    height, width = len(park), len(park[0])
    for row in range(height):
        for column in range(width):
            if park[row][column] == "S":
                current_row, current_column = row, column
    direction = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}
    for route in routes:
        command, raw_distance = route.split()
        distance = int(raw_distance)
        dr, dc = direction[command]
        path = [
            (current_row + dr * step, current_column + dc * step)
            for step in range(1, distance + 1)
        ]
        if all(0 <= row < height and 0 <= column < width and park[row][column] != "X" for row, column in path):
            current_row, current_column = path[-1]
    return [current_row, current_column]
