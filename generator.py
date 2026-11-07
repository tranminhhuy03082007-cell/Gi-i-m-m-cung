"""Sinh mê cung kiểm thử (có seed để tái lập)."""
import random
from maze import Maze, PATH, WALL, START, END


def generate(rows: int, cols: int, seed: int = 42, loop_ratio: float = 0.0) -> Maze:
    """Recursive Backtracker (cài bằng stack) -> mê cung hoàn hảo; loop_ratio > 0 đục thêm tường tạo chu trình."""
    rows += rows % 2 == 0   # kích thước phải lẻ
    cols += cols % 2 == 0
    rows, cols = max(rows, 5), max(cols, 5)
    rnd = random.Random(seed)
    grid = [[WALL] * cols for _ in range(rows)]
    grid[1][1] = PATH
    stack = [(1, 1)]
    steps = ((-2, 0), (0, 2), (2, 0), (0, -2))

    while stack:
        r, c = stack[-1]
        cand = [(dr, dc) for dr, dc in steps
                if 0 < r + dr < rows - 1 and 0 < c + dc < cols - 1 and grid[r + dr][c + dc] == WALL]
        if not cand:
            stack.pop()
            continue
        dr, dc = rnd.choice(cand)
        grid[r + dr // 2][c + dc // 2] = PATH   # phá tường giữa
        grid[r + dr][c + dc] = PATH
        stack.append((r + dr, c + dc))

    if loop_ratio > 0:
        walls = []
        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                if grid[r][c] != WALL:
                    continue
                horiz = r % 2 == 1 and c % 2 == 0 and grid[r][c - 1] == PATH and grid[r][c + 1] == PATH
                vert = r % 2 == 0 and c % 2 == 1 and grid[r - 1][c] == PATH and grid[r + 1][c] == PATH
                if horiz or vert:
                    walls.append((r, c))
        rnd.shuffle(walls)
        for r, c in walls[: int(len(walls) * loop_ratio)]:
            grid[r][c] = PATH

    start, end = (1, 1), (rows - 2, cols - 2)
    grid[1][1], grid[end[0]][end[1]] = START, END
    kind = f"(loop {loop_ratio:.0%})" if loop_ratio > 0 else "(hoàn hảo)"
    return Maze(grid, start, end, f"Random {rows}x{cols} {kind}")


def open_field(rows: int, cols: int) -> Maze:
    """Căn phòng trống không vật cản - trường hợp nhiều đường đi nhất."""
    grid = [[WALL if r in (0, rows - 1) or c in (0, cols - 1) else PATH for c in range(cols)]
            for r in range(rows)]
    grid[1][1], grid[rows - 2][cols - 2] = START, END
    return Maze(grid, (1, 1), (rows - 2, cols - 2), f"Open field {rows}x{cols}")
