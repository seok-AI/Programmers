"""여는 괄호를 스택에 저장.

복잡도: O(n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/12909/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(s):
    # 이 구현의 선택: 여는 괄호를 스택에 저장
    # 상태 정의: 현재 접두부의 열린 괄호 수에서 닫힌 괄호 수를 뺀 balance이다.
    # 핵심 불변식: 모든 유효한 접두부에서 balance는 음수가 아니며, 전체를 읽은 뒤에는 0이다.
    stack = []
    for char in s:
        if char == "(":
            stack.append(char)
        elif not stack:
            return False
        else:
            stack.pop()
    return not stack
