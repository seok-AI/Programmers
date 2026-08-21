"""직전 값과 다른 원소만 결과에 추가.

복잡도: O(n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(arr):
    # 이 구현의 선택: 직전 값과 다른 원소만 결과에 추가
    # 상태 정의: 지금까지 압축한 결과의 마지막 값만 기억한다.
    # 핵심 불변식: 결과에는 각 연속 구간의 첫 원소만 있고 마지막 값은 현재 구간의 값이다.
    answer = []
    for value in arr:
        if not answer or answer[-1] != value:
            answer.append(value)
    return answer
