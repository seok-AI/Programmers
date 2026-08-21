"""정답을 한 번 순회하며 세 패턴 점수를 동시에 누적.

복잡도: O(n) time, O(1) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42840/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(answers):
    # 이 구현의 선택: 정답을 한 번 순회하며 세 패턴 점수를 동시에 누적
    # 상태 정의: 세 수포자의 반복 패턴별 정답 일치 횟수를 센다.
    # 핵심 불변식: 문제 인덱스를 패턴 길이로 나눈 나머지가 그 사람이 찍은 현재 답의 위치이다.
    patterns = [[1, 2, 3, 4, 5], [2, 1, 2, 3, 2, 4, 2, 5], [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]]
    scores = [0, 0, 0]
    for index, answer in enumerate(answers):
        for student, pattern in enumerate(patterns):
            scores[student] += pattern[index % len(pattern)] == answer
    return [student + 1 for student, score in enumerate(scores) if score == max(scores)]
