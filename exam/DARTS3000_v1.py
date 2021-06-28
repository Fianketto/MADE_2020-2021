# input_file = open("Files/tst1.txt", "r")
# lines = input_file.readlines()
# set_count = int(lines[0])
set_count = int(input())
ans = [0 for i in range(set_count)]

for i in range(set_count):
    s_max = 0
    s_min = 0
    s_max_so_far = 0
    s_min_so_far = 0
    s_tot = 0
    # N, K = list(map(int, lines[i*2+1].strip().split(" ")))
    N, K = list(map(int, input().split(" ")))
    # print(i, ", N=", N, ", K=", K)
    # A = list(map(int, lines[i*2+2].strip().split(" ")))
    A = list(map(int, input().strip().split(" ")))
    # print(A)
    if K >= 0:
        for j in range(K - N + 1, K):
            # print(A[j], end=" ")
            s_max = max(0, s_max + A[j])
            s_max_so_far = max(s_max_so_far, s_max)
            # print("j=", j, "s_max=", s_max, "s_min=", s_min, "s_tot=", s_tot, "s_max_so_far=", s_max_so_far)
        # print("\nmax_sum=", s_max_so_far, "\n")
        ans[i] = s_max_so_far
    else:
        for j in range(N):
            # print(A[j], end=" ")
            s_max = max(0, s_max + A[j])
            s_min = min(0, s_min + A[j])
            s_tot += A[j]
            s_max_so_far = max(s_max_so_far, s_max)
            s_min_so_far = min(s_min_so_far, s_min)

            # print("j=", j, "s_max=", s_max, "s_min=", s_min, "s_tot=", s_tot)
        # print("\nmax_sum=", max(s_max_so_far, s_tot-s_min_so_far), "\n")
        ans[i] = max(s_max_so_far, s_tot - s_min_so_far)

for i in range(set_count):
    print(ans[i])
