"""현재 합별 경우의 수를 Counter로 압축.

복잡도: O(n*S) time, O(S) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import Counter

def solution(numbers, target):
    # 이 구현의 선택: 현재 합별 경우의 수를 Counter로 압축
    # 상태 정의: 지금까지의 숫자로 만들 수 있는 합별 경우의 수를 상태로 둔다.
    # 핵심 불변식: 숫자 하나를 처리한 뒤 새 상태는 이전 모든 합에 그 수를 더하거나 뺀 결과의 정확한 빈도이다.
    states = Counter({0: 1})
    for number in numbers:
        next_states = Counter()
        for total, count in states.items():
            next_states[total + number] += count
            next_states[total - number] += count
        states = next_states
    return states[target]
