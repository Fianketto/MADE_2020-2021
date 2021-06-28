import sys
import threading
sys.setrecursionlimit(10 ** 9)
threading.stack_size(10 ** 8)

FIRST_USER = "polycarp"
current_maximum = 1


def solve():
    def dfs(user, depth):
        global current_maximum
        if user in users_reposted:
            for next_user in users_reposted[user]:
                depth_on[next_user] = depth + 1
                current_maximum = max(current_maximum, depth + 1)
                dfs(next_user, depth + 1)

    m = int(sys.stdin.buffer.readline().decode())
    users_reposted = {}  # users_reposted["user2"] - список пользователей, которые репостнули user2
    depth_on = {}  # depth_on["user1"] - глубина репоста на пользователе user1
    for line in sys.stdin.buffer.read().decode().splitlines():
        repost_info = line.split()
        user1 = repost_info[0].lower()
        user2 = repost_info[2].lower()
        users_reposted[user2] = users_reposted.get(user2, []) + [user1]
        depth_on[user1] = 1

    dfs(FIRST_USER, 1)
    print(current_maximum)


def main():
    solve()


if __name__ == "__main__":
    threading.Thread(target=main).start()
