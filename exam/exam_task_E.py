set_count = int(input())

for set_n in range(set_count):
    order_main = {}
    order_arrive = {}
    order_start = {}
    order_finish = {}
    order_should_finish = {}

    clients = {}

    E, N, K = list(map(int, input().split(" ")))
    for i in range(E):
        a = input().split(" ")
        ord_id = a[1]
        if a[0] == "ordered":
            ord_user = a[2]
            ord_time = int(a[3])
            taxi_comes_in = int(a[4]) * 60
            ord_finishes_in = int(a[5]) * 60
            order_main[ord_id] = [ord_user, ord_time, taxi_comes_in, ord_finishes_in]
        elif a[0] == "arrived":
            arrive_time = int(a[2])
            order_arrive[ord_id] = int(arrive_time)
        elif a[0] == "started":
            start_time = int(a[2])
            order_start[ord_id] = int(start_time)
        elif a[0] == "finished":
            finish_time = int(a[2])
            order_finish[ord_id] = int(finish_time)

    # print(order_main)
    # print(order_arrive)
    # print(order_start)
    # print(order_finish)

    for ord_id in order_main.keys():
        if ord_id in order_arrive.keys() and ord_id in order_start.keys() and ord_id in order_finish.keys():
            order_finish_plan = order_main[ord_id][1] + order_main[ord_id][2] + order_main[ord_id][3] + K * 60
            order_finish_fact = order_finish[ord_id]
            if order_start[ord_id] - order_arrive[ord_id] <= K * 60:
                if order_finish_fact > order_finish_plan:
                    late_for = order_finish_fact - order_finish_plan
                    user_id = order_main[ord_id][0]
                    clients[user_id] = clients.get(user_id, 0) + late_for

    # print(clients)
    cl_keys = []
    cl_vals = []
    used_vals = []
    cl_keys_sorted = []
    ans = ""
    if bool(clients):
        printed = 0
        ans = ""
        for cl in clients.keys():
            cl_keys.append(cl)
            cl_vals.append(clients[cl])
        cl_vals.sort(reverse=True)

        for i in range(len(cl_vals)):
            next_val = cl_vals[i]
            temp_keys = []
            if next_val not in used_vals:
                used_vals.append(next_val)
                for k in cl_keys:
                    if clients[k] == next_val:
                        temp_keys.append(k)
                temp_keys.sort()
                for k in temp_keys:
                    cl_keys_sorted.append(k)
        # print(cl_keys_sorted)

        for k in cl_keys_sorted:
            if printed < N:
                if printed > 0:
                    ans += " "
                    # print(" ", end="", sep="")
                # print(i[0], end="", sep="")
                ans += k
                printed += 1
    else:
        ans = "-"
    print(ans)
