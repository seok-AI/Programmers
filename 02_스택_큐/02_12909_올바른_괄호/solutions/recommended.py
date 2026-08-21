"""접두 구간의 괄호 균형 유지.

복잡도: O(n) time, O(1) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(s):
    # 이 구현의 선택: 접두 구간의 괄호 균형 유지
    # 상태 정의: 현재 접두부의 열린 괄호 수에서 닫힌 괄호 수를 뺀 balance이다.
    # 핵심 불변식: 모든 유효한 접두부에서 balance는 음수가 아니며, 전체를 읽은 뒤에는 0이다.
    balance = 0
    for char in s:
        balance += 1 if char == "(" else -1
        # 닫는 괄호가 먼저 많아지면 이후 문자로 복구해도 올바른 접두부가 아니다.
        if balance < 0:
            return False
    return balance == 0
