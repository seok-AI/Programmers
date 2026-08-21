"""상하 이동 합과 연속 A 구간별 최소 좌우 이동 결합.

복잡도: O(n^2) time, O(1) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(name):
    # 이 구현의 선택: 상하 이동 합과 연속 A 구간별 최소 좌우 이동 결합
    # 상태 정의: 문자별 상하 조작 비용과, 커서가 방문해야 할 비-A 위치 구간을 분리한다.
    # 핵심 불변식: 연속 A 구간 하나를 건너뛰는 최적 경로는 한쪽을 한 번 되짚는 두 형태 중 하나이다.
    vertical = sum(min(ord(char) - ord("A"), ord("Z") - ord(char) + 1) for char in name)
    horizontal = len(name) - 1
    for index in range(len(name)):
        next_index = index + 1
        while next_index < len(name) and name[next_index] == "A":
            next_index += 1
        # 오른쪽으로 갔다 돌아오기 / 왼쪽으로 먼저 갔다 돌아오기 중 작은 값.
        horizontal = min(
            horizontal,
            2 * index + len(name) - next_index,
            index + 2 * (len(name) - next_index),
        )
    return vertical + horizontal
