"""모든 숫자 순열을 집합에 모아 소수 판정.

복잡도: O(sum P(n,k) * sqrt(M)) time, O(sum P(n,k)) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from itertools import permutations

def solution(numbers):
    # 이 구현의 선택: 모든 숫자 순열을 집합에 모아 소수 판정
    # 상태 정의: 사용한 숫자 인덱스 순열로 만든 모든 정수를 집합에 모은다.
    # 핵심 불변식: 집합은 선행 0이나 중복 숫자 순열이 만든 같은 정수를 한 번만 남긴다.
    candidates = set()
    for length in range(1, len(numbers) + 1):
        candidates.update(int("".join(digits)) for digits in permutations(numbers, length))

    def is_prime(value):
        if value < 2:
            return False
        if value % 2 == 0:
            return value == 2
        divisor = 3
        while divisor * divisor <= value:
            if value % divisor == 0:
                return False
            divisor += 2
        return True

    return sum(is_prime(value) for value in candidates)
