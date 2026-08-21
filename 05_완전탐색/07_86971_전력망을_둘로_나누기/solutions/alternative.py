"""트리를 한 번 순회해 각 자식 서브트리 크기 계산.

복잡도: O(n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/86971/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(n, wires):
    # 이 구현의 선택: 트리를 한 번 순회해 각 자식 서브트리 크기 계산
    # 상태 정의: 한 전선을 제외했을 때 임의의 한쪽 연결요소 크기를 센다.
    # 핵심 불변식: 트리에서 간선 하나를 끊으면 정확히 두 컴포넌트가 되고 크기 합은 n이다.
    graph = [[] for _ in range(n + 1)]
    for left, right in wires:
        graph[left].append(right)
        graph[right].append(left)

    answer = n

    def subtree(node, parent):
        nonlocal answer
        size = 1
        for neighbor in graph[node]:
            if neighbor != parent:
                size += subtree(neighbor, node)
        # 부모와 연결된 간선을 자르면 size 대 n-size로 나뉜다.
        if parent:
            answer = min(answer, abs(n - 2 * size))
        return size

    subtree(1, 0)
    return answer
