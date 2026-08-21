"""학생별 체육복 수 배열에서 왼쪽부터 부족분 전달.

복잡도: O(n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42862/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(n, lost, reserve):
    # 이 구현의 선택: 학생별 체육복 수 배열에서 왼쪽부터 부족분 전달
    # 상태 정의: 도난과 여벌이 겹친 학생을 먼저 제거한 뒤 실제 대여자·필요자 집합을 둔다.
    # 핵심 불변식: 앞 번호부터 처리할 때 왼쪽 이웃을 먼저 배정해도 뒤 학생의 가능한 선택을 줄이지 않는다.
    clothes = [1] * (n + 2)
    for student in lost:
        clothes[student] -= 1
    for student in reserve:
        clothes[student] += 1
    for student in range(1, n + 1):
        if clothes[student] == 0 and clothes[student - 1] == 2:
            clothes[student - 1] -= 1
            clothes[student] += 1
        elif clothes[student] == 0 and clothes[student + 1] == 2:
            clothes[student + 1] -= 1
            clothes[student] += 1
    return sum(clothes[student] >= 1 for student in range(1, n + 1))
