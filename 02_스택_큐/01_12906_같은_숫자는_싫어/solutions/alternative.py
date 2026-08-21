"""연속 그룹의 첫 원소 선택.

복잡도: O(n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/12906/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(arr):
    # 이 구현의 선택: 연속 그룹의 첫 원소 선택
    # 상태 정의: 지금까지 압축한 결과의 마지막 값만 기억한다.
    # 핵심 불변식: 결과에는 각 연속 구간의 첫 원소만 있고 마지막 값은 현재 구간의 값이다.
    if not arr:
        return []
    answer = [arr[0]]
    for previous, current in zip(arr, arr[1:]):
        if previous != current:
            answer.append(current)
    return answer
