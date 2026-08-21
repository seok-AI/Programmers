"""종류를 하나씩 추가하는 1상태 DP.

복잡도: O(n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42578/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import Counter

def solution(clothes):
    # 이 구현의 선택: 종류를 하나씩 추가하는 1상태 DP
    # 상태 정의: 의상 종류별 개수와 그 종류를 입지 않는 한 가지 선택을 센다.
    # 핵심 불변식: 처리한 종류들의 선택 조합 수에는 ‘모두 미선택’인 조합이 정확히 하나 포함된다.
    counts = Counter(kind for _, kind in clothes)
    ways = 1  # 아직 아무 종류도 처리하지 않았을 때 빈 선택 한 가지
    for count in counts.values():
        ways += ways * count
    return ways - 1
