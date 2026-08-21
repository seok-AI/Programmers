"""키패드 좌표의 맨해튼 거리와 주손 우선순위 비교.

복잡도: O(n) time, O(1) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(numbers, hand):
    # 이 구현의 선택: 키패드 좌표의 맨해튼 거리와 주손 우선순위 비교
    # 상태 정의: 왼손·오른손의 현재 키 좌표를 유지한다.
    # 핵심 불변식: 숫자 하나를 누른 뒤 해당 손의 위치만 그 키로 갱신된다.
    coordinates = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 9: (2, 2),
        "*": (3, 0), 0: (3, 1), "#": (3, 2),
    }
    left, right = "*", "#"
    answer = []
    for number in numbers:
        if number in (1, 4, 7):
            chosen = "L"
        elif number in (3, 6, 9):
            chosen = "R"
        else:
            target = coordinates[number]
            left_distance = sum(abs(a - b) for a, b in zip(coordinates[left], target))
            right_distance = sum(abs(a - b) for a, b in zip(coordinates[right], target))
            chosen = "L" if left_distance < right_distance or (left_distance == right_distance and hand == "left") else "R"
        answer.append(chosen)
        if chosen == "L":
            left = number
        else:
            right = number
    return "".join(answer)
