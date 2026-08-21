"""장르 집계 후 장르/곡 다중 정렬.

복잡도: O(n log n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import defaultdict

def solution(genres, plays):
    # 이 구현의 선택: 장르 집계 후 장르/곡 다중 정렬
    # 상태 정의: 장르별 총 재생 수와 장르 안의 (곡 재생 수, 고유 번호) 목록이다.
    # 핵심 불변식: 장르 순서는 총합 내림차순이고, 같은 장르 곡은 재생 수 내림차순·번호 오름차순이다.
    totals = defaultdict(int)
    songs = defaultdict(list)
    for index, (genre, play) in enumerate(zip(genres, plays)):
        totals[genre] += play
        songs[genre].append((play, index))

    answer = []
    for genre in sorted(totals, key=totals.get, reverse=True):
        # 재생 수 내림차순, 고유 번호 오름차순.
        songs[genre].sort(key=lambda item: (-item[0], item[1]))
        answer.extend(index for _, index in songs[genre][:2])
    return answer
