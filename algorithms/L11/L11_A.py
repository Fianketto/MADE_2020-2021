import sys


def inside_board(x, y):
    if -1 < x < n and -1 < y < n:
        return True
    return False


def bfs():
    path_found = False
    while len(queue_of_cells) > 0 and not path_found:
        cell = queue_of_cells.pop(0)
        for term in terms:
            neigh_i = cell[0] + term[0]
            neigh_j = cell[1] + term[1]
            if inside_board(neigh_i, neigh_j) and not cell_was_used[neigh_i][neigh_j]:
                queue_of_cells.append((neigh_i, neigh_j))
                cell_was_used[neigh_i][neigh_j] = True
                cells_parent[neigh_i][neigh_j] = (cell[0], cell[1])
            if (neigh_i, neigh_j) == destination:
                path_found = True
                break
    current_cell = destination
    while current_cell[0] > -1:
        i, j = current_cell[0], current_cell[1]
        ans.append((i + 1, j + 1))
        current_cell = cells_parent[i][j]
    ans.reverse()


n = int(sys.stdin.buffer.readline().decode())
starting_position = list(map(int, sys.stdin.buffer.readline().decode().split()))
starting_position = (starting_position[0] - 1, starting_position[1] - 1)
destination = list(map(int, sys.stdin.buffer.readline().decode().split()))
destination = (destination[0] - 1, destination[1] - 1)

cell_was_used = [[False for j in range(n)] for i in range(n)]
cells_parent = [[(-1, -1) for j in range(n)] for i in range(n)]

queue_of_cells = []
terms = []
for i in range(-1, 2, 2):
    for j in range(-2, 3, 4):
        terms.append((i, j))
        terms.append((j, i))

queue_of_cells.append(starting_position)
cell_was_used[starting_position[0]][starting_position[1]] = True

ans = []
bfs()
print(len(ans))
for cell in ans:
    print(cell[0], cell[1])
