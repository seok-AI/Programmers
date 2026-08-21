"""중복 상태 정리 후 앞번호부터 왼쪽 이웃 우선 대여.

복잡도: O(n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(n, lost, reserve):
    # 이 구현의 선택: 중복 상태 정리 후 앞번호부터 왼쪽 이웃 우선 대여
    # 상태 정의: 도난과 여벌이 겹친 학생을 먼저 제거한 뒤 실제 대여자·필요자 집합을 둔다.
    # 핵심 불변식: 앞 번호부터 처리할 때 왼쪽 이웃을 먼저 배정해도 뒤 학생의 가능한 선택을 줄이지 않는다.
    lost_set = set(lost) - set(reserve)
    reserve_set = set(reserve) - set(lost)
    for student in sorted(lost_set):
        for lender in (student - 1, student + 1):
            if lender in reserve_set:
                reserve_set.remove(lender)
                lost_set.remove(student)
                break
    return n - len(lost_set)
