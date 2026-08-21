"""1..k 점수 빈도로 높은 점수부터 상자 채우기.

복잡도: O(n+k) time, O(k) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/135808/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import Counter

def solution(k, m, score):
    # 이 구현의 선택: 1..k 점수 빈도로 높은 점수부터 상자 채우기
    # 상태 정의: 완전한 상자마다 포함된 최저 점수가 그 상자의 단가를 결정한다.
    # 핵심 불변식: 높은 점수부터 m개씩 묶으면 각 상자의 최솟값을 가능한 한 크게 만든다.
    counts = Counter(score)
    filled = answer = 0
    for value in range(k, 0, -1):
        for _ in range(counts[value]):
            filled += 1
            if filled == m:
                answer += value * m
                filled = 0
    return answer
