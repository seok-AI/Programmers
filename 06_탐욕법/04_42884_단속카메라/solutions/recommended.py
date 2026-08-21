"""진출 지점이 빠른 차량부터 그 지점에 카메라 설치.

복잡도: O(n log n) time, O(1) extra space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

import math

def solution(routes):
    # 이 구현의 선택: 진출 지점이 빠른 차량부터 그 지점에 카메라 설치
    # 상태 정의: 아직 카메라가 없는 경로 중 진출 지점이 가장 이른 경로의 진출점에 카메라를 둔다.
    # 핵심 불변식: 마지막 카메라 위치 이하에서 시작하는 모든 처리된 경로는 그 카메라와 교차한다.
    cameras = 0
    last_camera = -math.inf
    for entry, exit_point in sorted(routes, key=lambda route: route[1]):
        if last_camera < entry:
            last_camera = exit_point
            cameras += 1
    return cameras
