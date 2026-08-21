"""제거 횟수를 직접 세며 가능한 거리의 최댓값 저장.

복잡도: O(n log distance) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/43236/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(distance, rocks, n):
    # 이 구현의 선택: 제거 횟수를 직접 세며 가능한 거리의 최댓값 저장
    # 상태 정의: 후보 최소거리 d를 지키며 남길 수 없는 바위 수를 탐욕적으로 센다.
    # 핵심 불변식: 왼쪽부터 이전에 남긴 바위와 거리가 d 미만이면 현재 바위를 제거하는 것이 이후 선택 공간을 최대화한다.
    ordered = [0] + sorted(rocks) + [distance]
    left, right = 1, distance
    answer = 0
    while left <= right:
        gap = (left + right) // 2
        removals = 0
        last = ordered[0]
        for position in ordered[1:]:
            if position - last < gap:
                removals += 1
            else:
                last = position
        if removals <= n:
            answer = gap
            left = gap + 1
        else:
            right = gap - 1
    return answer
