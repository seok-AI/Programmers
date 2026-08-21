"""후보 도착점까지 한 칸씩 검사하고 실패 시 원위치.

복잡도: O(routes*distance) time, O(1) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/172928/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(park, routes):
    # 이 구현의 선택: 후보 도착점까지 한 칸씩 검사하고 실패 시 원위치
    # 상태 정의: 현재 로봇 좌표를 두고 명령 하나의 모든 중간 칸을 임시 검사한다.
    # 핵심 불변식: 명령이 끝까지 유효할 때만 현재 좌표가 목적지로 바뀌며, 하나라도 막히면 원위치이다.
    height, width = len(park), len(park[0])
    start = next((row, line.index("S")) for row, line in enumerate(park) if "S" in line)
    row, column = start
    moves = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}
    for route in routes:
        command, distance = route.split()
        dr, dc = moves[command]
        candidate_row, candidate_column = row, column
        valid = True
        for _ in range(int(distance)):
            candidate_row += dr
            candidate_column += dc
            if not (0 <= candidate_row < height and 0 <= candidate_column < width) or park[candidate_row][candidate_column] == "X":
                valid = False
                break
        if valid:
            row, column = candidate_row, candidate_column
    return [row, column]
