# 2024.10.09 16:20 시작
import sys
import math
import heapq

# sys.stdin = open("./input.txt", "r")


def dijkstra(graph, start):
    dp = [math.inf] * n
    dp[start] = 0
    pq = [(0, start)]
    visited = [False] * n

    while True:
        if len(pq) == 0:
            break

        dist, cur_node = heapq.heappop(pq)
        if visited[cur_node]:
            continue

        for next_node in graph[cur_node]:
            new_dist = dist + graph[cur_node][next_node]
            if new_dist < dp[next_node]:
                dp[next_node] = new_dist
                heapq.heappush(pq, (new_dist, next_node))

    return dp


def get_gains(trips, dists):
    new_gains = []

    for trip_id in trips:
        r, d = trips[trip_id]
        if dists[d] != math.inf and r >= dists[d]:
            heapq.heappush(new_gains, (-r + dists[d], trip_id))

    return new_gains


Q = int(input())
codetree_land = {}
start_node = 0
start_node_changed = True
distances = []
trips = {}
gains = []

for _ in range(Q):
    command = list(map(int, input().split()))

    # 코드트리 랜드 건설
    if command[0] == 100:
        n, m, edges = command[1], command[2], command[3:]
        codetree_land = {i: {} for i in range(n)}

        for index in range(m):
            v, u, w = edges[3 * index], edges[3 * index + 1], edges[3 * index + 2]
            if v == u:
                continue

            codetree_land[u][v] = min(codetree_land[u].get(v, math.inf), w)
            codetree_land[v][u] = min(codetree_land[v].get(u, math.inf), w)

    # 여행 상품 생성
    elif command[0] == 200:
        id, revenue, dest = command[1], command[2], command[3]
        trips[id] = (revenue, dest)

        if not start_node_changed:
            if distances[dest] != math.inf and revenue >= distances[dest]:
                heapq.heappush(gains, (-revenue + distances[dest], id))

    # 여행 상품 취소
    elif command[0] == 300:
        id = command[1]

        if id in trips:
            del trips[id]

    # 최적의 여행 상품 판매
    elif command[0] == 400:
        if start_node_changed:
            distances = dijkstra(codetree_land, start_node)
            gains = get_gains(trips, distances)
            start_node_changed = False

        id = -1
        while True:
            if len(gains) == 0:
                break

            _, new_id = heapq.heappop(gains)

            if new_id in trips:
                id = new_id
                break

        print(id)
        if id != -1:
            del trips[id]

    # 여행 상품의 출발지 변경
    elif command[0] == 500:
        s = command[1]
        if s != start_node:
            start_node = s
            start_node_changed = True