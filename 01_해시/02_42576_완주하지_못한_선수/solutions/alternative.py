"""두 목록 정렬 후 첫 불일치 탐색.

복잡도: O(n log n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42576/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(participant, completion):
    # 이 구현의 선택: 두 목록 정렬 후 첫 불일치 탐색
    # 상태 정의: 이름별 참가 횟수에서 완주 횟수를 뺀 잔여 빈도이다.
    # 핵심 불변식: 완주자를 한 명 처리할 때마다 그 이름의 미완주 후보 수가 정확히 1 감소한다.
    # 정렬하면 같은 이름이 나란히 오므로 처음 다른 위치가 미완주자다.
    participants = sorted(participant)
    completions = sorted(completion)
    for runner, finisher in zip(participants, completions):
        if runner != finisher:
            return runner
    return participants[-1]
