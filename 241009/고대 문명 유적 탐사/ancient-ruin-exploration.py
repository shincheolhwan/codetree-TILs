# 2024.10.09 12:02 시작
import sys
from queue import Queue

# sys.stdin = open('./input.txt', 'r')


def rotate_90(x, y):
    new_maps = []
    for i in range(N):
        new_maps.append(maps[i].copy())

    rotates = [[], [], []]
    for r in range(3):
        for c in range(3):
            rotates[r].append(new_maps[x + r - 1][y + c - 1])

    for r in range(3):
        for c in range(3):
            rotates[c][2 - r] = new_maps[x + r - 1][y + c - 1]

    for r in range(3):
        for c in range(3):
            new_maps[x + r - 1][y + c - 1] = rotates[r][c]

    return new_maps


def rotate_180(x, y):
    new_maps = []
    for i in range(N):
        new_maps.append(maps[i].copy())

    rotates = [[], [], []]
    for r in range(3):
        for c in range(3):
            rotates[r].append(new_maps[x + r - 1][y + c - 1])

    for r in range(3):
        for c in range(3):
            rotates[2 - r][2 - c] = new_maps[x + r - 1][y + c - 1]

    for r in range(3):
        for c in range(3):
            new_maps[x + r - 1][y + c - 1] = rotates[r][c]

    return new_maps


def rotate_270(x, y):
    new_maps = []
    for i in range(N):
        new_maps.append(maps[i].copy())

    rotates = [[], [], []]
    for r in range(3):
        for c in range(3):
            rotates[r].append(new_maps[x + r - 1][y + c - 1])

    for r in range(3):
        for c in range(3):
            rotates[2 - c][r] = new_maps[x + r - 1][y + c - 1]

    for r in range(3):
        for c in range(3):
            new_maps[x + r - 1][y + c - 1] = rotates[r][c]

    return new_maps


def get_pop_points(m, start_points):
    visited = [[False] * N for _ in range(N)]
    pop_points = []
    for x, y in start_points:
        if visited[x][y]:
            continue

        q = Queue()
        q.put((x, y))
        visited[x][y] = True
        pops = [(x, y)]

        while True:
            if q.empty():
                break

            cur_x, cur_y = q.get()

            for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                next_x, next_y = cur_x + dx, cur_y + dy
                # 경계값 조건
                if 0 <= next_x < N and 0 <= next_y < N:
                    # 방문 했는지
                    if not visited[next_x][next_y]:
                        # 같은 숫자
                        if m[x][y] == m[next_x][next_y]:
                            q.put((next_x, next_y))
                            visited[next_x][next_y] = True
                            pops.append((next_x, next_y))

        if len(pops) >= 3:
            pop_points += pops
    return pop_points


def compare_rotate(score1, score2, degree1, degree2, center1, center2):
    # 스코어 비교
    if score1 > score2:
        return 0
    elif score2 > score1:
        return 1

    # 각도 비교
    if degree1 < degree2:
        return 0
    elif degree2 < degree1:
        return 1

    # 열 비교
    if center1[1] < center2[1]:
        return 0
    elif center2[1] < center1[1]:
        return 1

    # 행 비교
    if center1[0] < center2[0]:
        return 0
    elif center2[0] < center1[0]:
        return 1
    else:
        print(score1, score2)
        print(degree1, degree2)
        print(center1[1], center2[1])
        print(center1[0], center2[0])
        print("compare rotate error")


def get_first_score():
    m = None
    p = []
    score = 0
    degree = 360
    c_x = 4
    c_y = 4

    for center_x in range(1, N - 1):
        for center_y in range(1, N - 1):
            change_points = []
            for i in range(3):
                for j in range(3):
                    change_points.append((center_x + i - 1, center_y + j - 1))

            new_maps = rotate_90(center_x, center_y)
            points = get_pop_points(new_maps, change_points)
            if compare_rotate(score, len(points), degree, 90, (c_x, c_y), (center_x, center_y)):
                m = new_maps
                p = points
                score = len(points)
                degree = 90
                c_x = center_x
                c_y = center_y

            new_maps = rotate_180(center_x, center_y)
            points = get_pop_points(new_maps, change_points)
            if compare_rotate(score, len(points), degree, 180, (c_x, c_y), (center_x, center_y)):
                m = new_maps
                p = points
                score = len(points)
                degree = 180
                c_x = center_x
                c_y = center_y

            new_maps = rotate_270(center_x, center_y)
            points = get_pop_points(new_maps, change_points)
            if compare_rotate(score, len(points), degree, 270, (c_x, c_y), (center_x, center_y)):
                m = new_maps
                p = points
                score = len(points)
                degree = 270
                c_x = center_x
                c_y = center_y

    return m, p, score


N = 5
K, M = map(int, input().split())
maps = []
for _ in range(N):
    maps.append(list(map(int, input().split())))

items = list(map(int, input().split()))
items.reverse()
scores = []

for _ in range(K):
    cur_score = 0
    maps, points, score = get_first_score()

    if score == 0:
        break

    cur_score += score

    while True:
        points.sort(key=lambda p: (p[1], -p[0]))
        for point in points:
            maps[point[0]][point[1]] = items.pop()

        points = get_pop_points(maps, points)

        if len(points) == 0:
            break
        else:
            cur_score += len(points)

    scores.append(cur_score)

print(*scores)