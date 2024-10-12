# 2024.10.12 20:32 시작
import sys
from queue import Queue

# sys.stdin = open("input.txt", "r")


class Team:
    def __init__(self, head_x, head_y, tail_x, tail_y, length):
        self.head_x = head_x
        self.head_y = head_y
        self.tail_x = tail_x
        self.tail_y = tail_y
        self.length = length

    def change_head_tail(self):
        temp_x = self.head_x
        temp_y = self.head_y
        self.head_x = self.tail_x
        self.head_y = self.tail_y
        self.tail_x = temp_x
        self.tail_y = temp_y

        maps[self.head_x][self.head_y] = 1
        maps[self.tail_x][self.tail_y] = 3


dxs = [1, 0, -1, 0]
dys = [0, 1, 0, -1]


def find_tail(x, y):
    visited = [[False] * n for _ in range(n)]
    q = Queue()
    q.put((x, y, 1))
    visited[x][y] = True

    while True:
        if q.empty():
            break

        cur_x, cur_y, length = q.get()
        for dx, dy in zip(dxs, dys):
            next_x, next_y, next_length = cur_x + dx, cur_y + dy, length + 1
            if 0 <= next_x < n and 0 <= next_y < n:
                if visited[next_x][next_y]:
                    continue

                if maps[next_x][next_y] == 2:
                    visited[next_x][next_y] = True
                    q.put((next_x, next_y, next_length))
                elif maps[next_x][next_y] == 3:
                    return next_x, next_y, next_length


def get_score(x, y):
    if maps[x][y] == 1:
        team, _ = find_team(x, y)
        team.change_head_tail()
        return 1
    elif maps[x][y] == 2:
        visited = [[False] * n for _ in range(n)]
        q = Queue()
        q.put((x, y, 1))
        visited[x][y] = True

        while True:
            if q.empty():
                break

            cur_x, cur_y, count = q.get()
            for dx, dy in zip(dxs, dys):
                next_x, next_y, next_count = cur_x + dx, cur_y + dy, count + 1
                if 0 <= next_x < n and 0 <= next_y < n:
                    if visited[next_x][next_y]:
                        continue

                    if maps[next_x][next_y] == 1:
                        team, _ = find_team(next_x, next_y)
                        team.change_head_tail()
                        return next_count ** 2

                    elif maps[next_x][next_y] == 2:
                        visited[next_x][next_y] = True
                        q.put((next_x, next_y))

                    elif maps[next_x][next_y] == 3:
                        team, _ = find_team(next_x, next_y)
                        team.change_head_tail()
                        return (team.length + 1 - next_count) ** 2

    elif maps[x][y] == 3:
        team, _ = find_team(x, y)
        team.change_head_tail()
        return team.length ** 2
    else:
        print("get_score error")


def find_team(x, y):
    for team in teams:
        if team.head_x == x and team.head_y == y:
            return team, 1
        elif team.tail_x == x and team.tail_y == y:
            return team, 3


def move_team(team):
    visited = [[False] * n for _ in range(n)]
    q = Queue()
    q.put((team.tail_x, team.tail_y, 3))
    visited[team.tail_x][team.tail_y] = True
    maps[team.tail_x][team.tail_y] = 4

    while True:
        if q.empty():
            break

        cur_x, cur_y, role = q.get()
        for dx, dy in zip(dxs, dys):
            next_x, next_y = cur_x + dx, cur_y + dy
            if 0 <= next_x < n and 0 <= next_y < n:
                if visited[next_x][next_y]:
                    continue

                if maps[next_x][next_y] == 1:
                    visited[next_x][next_y] = True
                    maps[next_x][next_y] = role
                    if role == 3:
                        team.tail_x = next_x
                        team.tail_y = next_y

                    q.put((next_x, next_y, 1))
                elif maps[next_x][next_y] == 2:
                    visited[next_x][next_y] = True
                    maps[next_x][next_y] = role
                    if role == 3:
                        team.tail_x = next_x
                        team.tail_y = next_y
                    q.put((next_x, next_y, 2))
                elif role == 1 and maps[next_x][next_y] == 4:
                    maps[next_x][next_y] = 1
                    team.head_x = next_x
                    team.head_y = next_y


def throw_ball(turn):
    turn %= 4 * n

    # 왼쪽 -> 오른쪽
    if 0 <= turn < n:
        r = turn % n
        for c in range(n):
            if maps[r][c] == 1 or maps[r][c] == 2 or maps[r][c] == 3:
                score = get_score(r, c)
                return score
    # 아래 -> 위
    elif n <= turn < 2 * n:
        c = turn % n
        for r in range(n - 1, -1, -1):
            if maps[r][c] == 1 or maps[r][c] == 2 or maps[r][c] == 3:
                score = get_score(r, c)
                return score
    # 오른쪽 -> 왼쪽
    elif 2 * n <= turn < 3 * n:
        r = n - 1 - turn % n
        for c in range(n - 1, -1, -1):
            if maps[r][c] == 1 or maps[r][c] == 2 or maps[r][c] == 3:
                score = get_score(r, c)
                return score
    # 위 -> 아래
    elif 3 * n <= turn < 4 * n:
        c = n - 1 - turn % n
        for r in range(n):
            if maps[r][c] == 1 or maps[r][c] == 2 or maps[r][c] == 3:
                score = get_score(r, c)
                return score

    return 0


# 격자의 크기 n, 팀의 개수 m, 라운드 수 k
n, m, k = map(int, input().split())

maps = []

for _ in range(n):
    maps.append(list(map(int, input().split())))

teams = []
for i in range(n):
    for j in range(n):
        # head 를 찾았을 때
        if maps[i][j] == 1:
            tail_x, tail_y, length = find_tail(i, j)
            teams.append(Team(i, j, tail_x, tail_y, length))

# for team in teams:
#     print(f"head: {team.head_x, team.head_y}, tail: {team.tail_x, team.tail_y}, length: {team.length}")

total_score = 0
for t in range(k):
    # print(f"-----------round {t}-----------")
    for team in teams:
        move_team(team)

    # for row in maps:
    #     print(*row)

    total_score += throw_ball(t)

    # for team in teams:
    #     print(f"head: {team.head_x, team.head_y}, tail: {team.tail_x, team.tail_y}")
print(total_score)