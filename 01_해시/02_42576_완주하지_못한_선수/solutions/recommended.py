"""Counter로 참가/완주 빈도 차감.

복잡도: O(n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import Counter

def solution(participant, completion):
    # 이 구현의 선택: Counter로 참가/완주 빈도 차감
    # 상태 정의: 이름별 참가 횟수에서 완주 횟수를 뺀 잔여 빈도이다.
    # 핵심 불변식: 완주자를 한 명 처리할 때마다 그 이름의 미완주 후보 수가 정확히 1 감소한다.
    # 동명이인을 보존하려면 집합이 아니라 이름별 등장 횟수가 필요하다.
    remaining = Counter(participant)
    remaining.subtract(completion)

    # 정확히 한 사람만 남는다는 입력 보장이 있다.
    return next(name for name, count in remaining.items() if count > 0)
