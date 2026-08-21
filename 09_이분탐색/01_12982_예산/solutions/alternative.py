"""정렬한 금액의 누적합에서 예산의 삽입 위치 탐색.

복잡도: O(n log n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/12982/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from bisect import bisect_left

def solution(d, budget):
    # 이 구현의 선택: 정렬한 금액의 누적합에서 예산의 삽입 위치 탐색
    # 상태 정의: 현재까지 선택한 부서 수와 사용 예산을 유지한다.
    # 핵심 불변식: 같은 수의 부서를 지원할 때 가장 작은 신청액부터 고른 합이 최소이다.
    totals = []
    running = 0
    for request in sorted(d):
        running += request
        totals.append(running)
    return bisect_left(totals, budget + 1)
