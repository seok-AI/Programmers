"""겹치는 차량 구간의 교집합을 유지.

복잡도: O(n log n) time, O(1) extra space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42884/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(routes):
    # 이 구현의 선택: 겹치는 차량 구간의 교집합을 유지
    # 상태 정의: 아직 카메라가 없는 경로 중 진출 지점이 가장 이른 경로의 진출점에 카메라를 둔다.
    # 핵심 불변식: 마지막 카메라 위치 이하에서 시작하는 모든 처리된 경로는 그 카메라와 교차한다.
    ordered = sorted(routes)
    cameras = 1
    intersection_end = ordered[0][1]
    for entry, exit_point in ordered[1:]:
        if entry > intersection_end:
            cameras += 1
            intersection_end = exit_point
        else:
            intersection_end = min(intersection_end, exit_point)
    return cameras
