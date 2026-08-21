"""반복문으로 1기반 명령을 명시적으로 변환.

복잡도: O(q*k log k) time, O(k) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42748/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(array, commands):
    # 이 구현의 선택: 반복문으로 1기반 명령을 명시적으로 변환
    # 상태 정의: 각 명령은 서로 독립인 [자를 시작, 끝, 정렬 뒤 위치]이다.
    # 핵심 불변식: 원본 배열을 바꾸지 않은 슬라이스에는 해당 명령의 범위 원소만 들어간다.
    answer = []
    for start, end, rank in commands:
        section = list(array[start - 1 : end])
        section.sort()
        answer.append(section[rank - 1])
    return answer
