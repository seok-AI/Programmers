"""던전 순열을 만들고 각 순서의 실행 가능 접두부 측정.

복잡도: O(n!*n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/87946/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from itertools import permutations

def solution(k, dungeons):
    # 이 구현의 선택: 던전 순열을 만들고 각 순서의 실행 가능 접두부 측정
    # 상태 정의: 현재 피로도, 방문한 던전 집합, 지금까지 방문 수를 DFS 상태로 둔다.
    # 핵심 불변식: 재귀 경로에서 방문 표시는 그 경로가 선택한 던전과 정확히 일치한다.
    best = 0
    for order in permutations(dungeons):
        fatigue = k
        cleared = 0
        for required, cost in order:
            if fatigue < required:
                break
            fatigue -= cost
            cleared += 1
        best = max(best, cleared)
    return best
