"""n번째 문자와 전체 문자열의 복합 키.

복잡도: O(m log m) time, O(m) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(strings, n):
    # 이 구현의 선택: n번째 문자와 전체 문자열의 복합 키
    # 상태 정의: 문자열의 n번째 문자와 문자열 전체를 한 쌍의 정렬 키로 사용한다.
    # 핵심 불변식: 첫 키가 같을 때 전체 문자열 오름차순이 동률을 정확히 해소한다.
    return sorted(strings, key=lambda word: (word[n], word))
