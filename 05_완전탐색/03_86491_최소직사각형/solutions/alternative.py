"""필요할 때만 명함을 회전하며 지갑 치수 갱신.

복잡도: O(n) time, O(1) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/86491/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(sizes):
    # 이 구현의 선택: 필요할 때만 명함을 회전하며 지갑 치수 갱신
    # 상태 정의: 각 명함의 긴 변을 한 축, 짧은 변을 다른 축으로 통일한다.
    # 핵심 불변식: 지금까지 본 명함은 긴 변 최댓값 × 짧은 변 최댓값 지갑에 모두 들어간다.
    wallet_width = wallet_height = 0
    for width, height in sizes:
        if width < height:
            width, height = height, width
        wallet_width = max(wallet_width, width)
        wallet_height = max(wallet_height, height)
    return wallet_width * wallet_height
