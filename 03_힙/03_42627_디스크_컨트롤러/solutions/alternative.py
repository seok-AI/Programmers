"""매 시점 가능한 작업을 선형 선택.

복잡도: O(n^2) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42627/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(jobs):
    # 이 구현의 선택: 매 시점 가능한 작업을 선형 선택
    # 상태 정의: 현재 시각까지 요청된 작업을 실행 시간 기준 최소 힙에 둔다.
    # 핵심 불변식: 힙에는 이미 도착했지만 시작하지 않은 작업만 있고, 루트가 다음 SJF 작업이다.
    remaining = [(request, duration, index) for index, (request, duration) in enumerate(jobs)]
    time = total = 0
    while remaining:
        available = [job for job in remaining if job[0] <= time]
        if not available:
            time = min(request for request, _, _ in remaining)
            available = [job for job in remaining if job[0] <= time]
        chosen = min(available, key=lambda job: (job[1], job[0], job[2]))
        remaining.remove(chosen)
        request, duration, _ = chosen
        time += duration
        total += time - request
    return total // len(jobs)
