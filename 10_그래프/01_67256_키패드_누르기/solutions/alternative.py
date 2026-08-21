"""키패드 인덱스의 행·열 차이로 거리 계산.

복잡도: O(n) time, O(1) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/67256/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(numbers, hand):
    # 이 구현의 선택: 키패드 인덱스의 행·열 차이로 거리 계산
    # 상태 정의: 왼손·오른손의 현재 키 좌표를 유지한다.
    # 핵심 불변식: 숫자 하나를 누른 뒤 해당 손의 위치만 그 키로 갱신된다.
    # *, 0, #을 각각 10, 11, 12로 보면 3열 격자의 행/열 계산이 가능하다.
    def position(key):
        key = 11 if key == 0 else key
        return divmod(key - 1, 3)

    left, right = 10, 12
    preferred = "L" if hand == "left" else "R"
    answer = []
    for number in numbers:
        key = 11 if number == 0 else number
        if key % 3 == 1:
            press = "L"
        elif key % 3 == 0:
            press = "R"
        else:
            target = position(key)
            left_distance = sum(abs(a - b) for a, b in zip(position(left), target))
            right_distance = sum(abs(a - b) for a, b in zip(position(right), target))
            press = preferred if left_distance == right_distance else ("L" if left_distance < right_distance else "R")
        answer.append(press)
        if press == "L":
            left = key
        else:
            right = key
    return "".join(answer)
