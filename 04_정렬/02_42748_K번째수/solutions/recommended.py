"""명령별 슬라이스 정렬.

복잡도: O(q*k log k) time, O(k) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(array, commands):
    # 이 구현의 선택: 명령별 슬라이스 정렬
    # 상태 정의: 각 명령은 서로 독립인 [자를 시작, 끝, 정렬 뒤 위치]이다.
    # 핵심 불변식: 원본 배열을 바꾸지 않은 슬라이스에는 해당 명령의 범위 원소만 들어간다.
    return [sorted(array[start - 1 : end])[rank - 1] for start, end, rank in commands]
