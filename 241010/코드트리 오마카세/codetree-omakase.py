# 2024.10.10 20:01 시작
import sys

# sys.stdin = open('input.txt', 'r')


def eat_sushi(t):
    count = 0
    names = list(customers.keys())

    for name in names:
        customer = customers[name]
        sit_t = customer[0]
        sit_x = customer[1]

        # 나온 초밥이 있을 때
        if name in sushi:
            dishes = sushi[name]
            remain_dishes = []

            for dish in dishes:
                dish_t = dish[0]

                if dish_t < sit_t:
                    start_x = dish[1] + sit_t - dish_t
                    end_x = dish[1] + t - dish_t
                else:
                    start_x = dish[1]
                    end_x = dish[1] + t - dish_t

                temp = L * (start_x // L)
                # print(f"start_x:{start_x} end_x:{end_x} sit_x:{sit_x}")
                if (
                        (end_x - start_x >= L)
                        or (start_x - temp <= sit_x <= end_x - temp)
                ):
                    count += 1
                    customer[2] -= 1

                    if customer[2] == 0:
                        del customers[name]
                else:
                    remain_dishes.append(dish)

            if len(remain_dishes) > 0:
                sushi[name] = remain_dishes
            else:
                del sushi[name]

        # 나온 초밥이 없을 때
        else:
            continue

    return count


# L : 초밥 벨트의 길이
# Q: 명령의 수
L, Q = map(int, input().split())

sushi = {}
customers = {}
dish_count = 0

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
        dish_count += 1
    # 손님 입장
    elif code == 200:
        t, x, name, n = int(commands[1]), int(commands[2]), commands[3], int(commands[4])
        # 시간, 위치, 개수
        customers[name] = [t, x, n]
    # 사진 촬영
    elif code == 300:
        t = int(commands[1])
        eat_count = eat_sushi(t)
        dish_count -= eat_count
        print(len(customers), dish_count)