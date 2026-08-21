"""수포자별 주기 패턴을 나머지 인덱스로 비교.

복잡도: O(n) time, O(1) extra space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(answers):
    # 이 구현의 선택: 수포자별 주기 패턴을 나머지 인덱스로 비교
    # 상태 정의: 세 수포자의 반복 패턴별 정답 일치 횟수를 센다.
    # 핵심 불변식: 문제 인덱스를 패턴 길이로 나눈 나머지가 그 사람이 찍은 현재 답의 위치이다.
    patterns = (
        (1, 2, 3, 4, 5),
        (2, 1, 2, 3, 2, 4, 2, 5),
        (3, 3, 1, 1, 2, 2, 4, 4, 5, 5),
    )
    scores = [
        sum(answer == pattern[index % len(pattern)] for index, answer in enumerate(answers))
        for pattern in patterns
    ]
    best = max(scores)
    return [index + 1 for index, score in enumerate(scores) if score == best]
