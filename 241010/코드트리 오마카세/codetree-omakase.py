# 2024.10.10 20:01 시작
# 못 풀었음
import sys

# sys.stdin = open('input.txt', 'r')


def eat_sushi():
    count = 0
    names = list(customers.keys())

    for name in names:
        customer = customers[name]
        dishes = sushi[name]

        sit_t = customer[0]
        sit_x = customer[1]
        exit_time = -1

        for dish in dishes:
            dish_t = dish[0]
            dish_x = dish[1]

            # 음식이 먼저 나왔을 때
            if dish_t < sit_t:
                start_x = (dish_x + sit_t - dish_t) % L
                eat_time = sit_t + (sit_x + L - start_x) % L
            # 음식이 나중에 나왔을 때
            else:
                start_x = dish[1]
                eat_time = dish_t + (sit_x + L - start_x) % L
            exit_time = max(exit_time, eat_time)
            queries.append((111, eat_time))

        queries.append((222, exit_time))

    return count


# L : 초밥 벨트의 길이
# Q: 명령의 수
L, Q = map(int, input().split())

sushi = {}
customers = {}
queries = []

for _ in range(Q):
    commands = input().split()
    code = int(commands[0])

    # 초밥 만들기
    if code == 100:
        t, x, name = int(commands[1]), int(commands[2]), commands[3]
        if name not in sushi:
            sushi[name] = []
            pass
        # 시간, 위치
        sushi[name].append([t, x])
        queries.append((100, t))
    # 손님 입장
    elif code == 200:
        t, x, name, n = int(commands[1]), int(commands[2]), commands[3], int(commands[4])
        # 시간, 위치, 개수
        customers[name] = [t, x, n]
        queries.append((200, t))
    # 사진 촬영
    elif code == 300:
        t = int(commands[1])
        queries.append((300, t))

eat_sushi()
queries.sort(key=lambda query: (query[1], query[0]))

dish_count = 0
customer_count = 0

for q in queries:
    # print(q[0], q[1])
    if q[0] == 100:
        dish_count += 1
    elif q[0] == 111:
        dish_count -= 1
    elif q[0] == 200:
        customer_count += 1
    elif q[0] == 222:
        customer_count -= 1
    elif q[0] == 300:
        print(f"{customer_count} {dish_count}")