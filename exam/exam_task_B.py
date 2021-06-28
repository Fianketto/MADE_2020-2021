set_count = int(input())
ans = [0 for i in range(set_count)]

for set_n in range(set_count):
    point_count = int(input())
    per = []
    points_x = {}
    points_y = {}
    for point_n in range(point_count):
        point_info = list(map(int, input().split(" ")))
        per.append(point_info)
        points_x[point_info[0]] = points_x.get(point_info[0], 0) + 1
        points_y[point_info[1]] = points_y.get(point_info[1], 0) + 1

    n = len(per)
    sq_count = 0

    new_per = []
    for i in range(n):
        if points_x[per[i][0]] > 1 and points_y[per[i][1]] > 1:
            new_per.append([per[i][0], per[i][1]])
    n_new = len(new_per)

    dict_y = {}
    list_y = []
    for i in range(n_new):
        next_key = new_per[i][1]
        if next_key in dict_y.keys():
            dict_y[next_key].add(new_per[i][0])
        else:
            dict_y[next_key] = {new_per[i][0]}
    for y in dict_y.keys():
        list_y_el = dict_y[y].copy()
        list_y.append(list_y_el)

    for m in range(len(list_y)):
        if len(list_y[m]) > 1:
            for i in list_y[m]:
                for j in list_y[m]:
                    for k in range(m + 1, len(list_y)):
                        if i in list_y[k] and j in list_y[k] and i != j:
                            sq_count += 1
    ans[set_n] = sq_count / 2

for set_n in range(set_count):
    print(int(ans[set_n]))
