"""전체 인덱스를 장르 총합/곡 재생수로 한 번 정렬.

복잡도: O(n log n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42579/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import Counter

def solution(genres, plays):
    # 이 구현의 선택: 전체 인덱스를 장르 총합/곡 재생수로 한 번 정렬
    # 상태 정의: 장르별 총 재생 수와 장르 안의 (곡 재생 수, 고유 번호) 목록이다.
    # 핵심 불변식: 장르 순서는 총합 내림차순이고, 같은 장르 곡은 재생 수 내림차순·번호 오름차순이다.
    totals = Counter()
    for genre, play in zip(genres, plays):
        totals[genre] += play

    ordered = sorted(
        range(len(genres)),
        key=lambda i: (-totals[genres[i]], -plays[i], i),
    )
    used = Counter()
    answer = []
    for index in ordered:
        genre = genres[index]
        if used[genre] < 2:
            answer.append(index)
            used[genre] += 1
    return answer
