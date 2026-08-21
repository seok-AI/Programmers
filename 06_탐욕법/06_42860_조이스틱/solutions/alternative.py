"""바꿔야 할 위치 사이의 가장 긴 미방문 A 구간을 조사.

복잡도: O(n^2) time, O(1) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42860/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(name):
    # 이 구현의 선택: 바꿔야 할 위치 사이의 가장 긴 미방문 A 구간을 조사
    # 상태 정의: 문자별 상하 조작 비용과, 커서가 방문해야 할 비-A 위치 구간을 분리한다.
    # 핵심 불변식: 연속 A 구간 하나를 건너뛰는 최적 경로는 한쪽을 한 번 되짚는 두 형태 중 하나이다.
    change = sum(min(ord(char) - 65, 91 - ord(char)) for char in name)
    move = max(0, len(name) - 1)
    for left in range(len(name)):
        right = left + 1
        while right < len(name) and name[right] == "A":
            right += 1
        tail = len(name) - right
        move = min(move, left * 2 + tail, left + tail * 2)
    return change + move
