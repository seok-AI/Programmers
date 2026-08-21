"""정렬 리스트를 k개 이하로 유지.

복잡도: O(n*k) time, O(k) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/138477/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from bisect import insort

def solution(k, score):
    # 이 구현의 선택: 정렬 리스트를 k개 이하로 유지
    # 상태 정의: 현재까지의 상위 k개 점수만 최소 힙에 보관한다.
    # 핵심 불변식: 힙이 k개라면 루트는 현재까지 상위 k개 중 가장 낮은 발표 점수이다.
    hall = []
    answer = []
    for value in score:
        insort(hall, value)
        if len(hall) > k:
            hall.pop(0)
        answer.append(hall[0])
    return answer
