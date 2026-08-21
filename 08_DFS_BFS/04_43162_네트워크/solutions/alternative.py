"""연결 행렬의 간선을 Union-Find로 병합.

복잡도: O(n^2 alpha(n)) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/43162/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(n, computers):
    # 이 구현의 선택: 연결 행렬의 간선을 Union-Find로 병합
    # 상태 정의: 방문한 컴퓨터 집합과 현재 DFS가 덮는 하나의 연결요소를 구분한다.
    # 핵심 불변식: DFS가 끝나면 시작 컴퓨터와 경로로 연결된 모든 컴퓨터가 방문 상태이다.
    parent = list(range(n))

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    for left in range(n):
        for right in range(left + 1, n):
            if computers[left][right]:
                root_left, root_right = find(left), find(right)
                if root_left != root_right:
                    parent[root_right] = root_left
    return len({find(node) for node in range(n)})
