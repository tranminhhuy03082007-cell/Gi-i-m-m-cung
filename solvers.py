"""BFS (Queue), DFS lặp (Stack), DFS đệ quy. Mê cung là đồ thị: V = R*C, E <= 2V => O(R*C)."""
from __future__ import annotations
import sys
import threading
import time
from collections import deque
from maze import Maze, SolveResult, WALL, Point

# Thứ tự hướng: Lên, Phải, Xuống, Trái
DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def _neighbors(m: Maze, cur: int):
    """Sinh các ô kề đi được dưới dạng chỉ số phẳng."""
    cols = m.cols
    r, c = divmod(cur, cols)
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < m.rows and 0 <= nc < cols and m.grid[nr][nc] != WALL:
            yield nr * cols + nc


def _rebuild(parent: list[int], s: int, e: int, cols: int) -> list[Point]:
    """Lần ngược từ End về Start theo mảng cha rồi đảo lại."""
    path, cur = [], e
    while cur != -1:
        path.append(divmod(cur, cols))
        if cur == s:
            break
        cur = parent[cur]
    path.reverse()
    return path


def bfs(m: Maze) -> SolveResult:
    """BFS dùng deque làm hàng đợi -> đường ĐI NGẮN NHẤT. Thời gian/không gian O(R*C)."""
    t0 = time.perf_counter()
    cols, n = m.cols, m.cell_count
    parent = [-1] * n
    visited = [False] * n
    s = m.start[0] * cols + m.start[1]
    e = m.end[0] * cols + m.end[1]

    queue = deque([s])
    visited[s] = True          # đánh dấu ngay khi đưa vào hàng đợi
    count, peak, found = 0, 1, False

    while queue:
        peak = max(peak, len(queue))
        cur = queue.popleft()
        count += 1
        if cur == e:
            found = True
            break
        for nb in _neighbors(m, cur):
            if not visited[nb]:
                visited[nb] = True
                parent[nb] = cur
                queue.append(nb)

    path = _rebuild(parent, s, e, cols) if found else []
    return SolveResult("BFS (Queue)", found, path, count, peak,
                       (time.perf_counter() - t0) * 1000, visited, cols)


def dfs_iterative(m: Maze) -> SolveResult:
    """DFS dùng Stack tường minh (list), không lo tràn call stack. Không đảm bảo ngắn nhất."""
    t0 = time.perf_counter()
    cols, n = m.cols, m.cell_count
    parent = [-1] * n
    visited = [False] * n
    s = m.start[0] * cols + m.start[1]
    e = m.end[0] * cols + m.end[1]

    stack = [s]
    count, peak, found = 0, 1, False

    while stack:
        peak = max(peak, len(stack))
        cur = stack.pop()
        if visited[cur]:            # một ô có thể bị push nhiều lần
            continue
        visited[cur] = True         # đánh dấu khi pop để đúng thứ tự DFS
        count += 1
        if cur == e:
            found = True
            break
        # push ngược để hướng đầu tiên được pop trước (cùng thứ tự với bản đệ quy)
        for nb in reversed(list(_neighbors(m, cur))):
            if not visited[nb]:
                parent[nb] = cur
                stack.append(nb)

    path = _rebuild(parent, s, e, cols) if found else []
    return SolveResult("DFS (Stack)", found, path, count, peak,
                       (time.perf_counter() - t0) * 1000, visited, cols)


def dfs_recursive(m: Maze) -> SolveResult:
    """DFS đệ quy. Chạy trong thread có stack lớn và tăng recursion limit để chịu được mê cung lớn."""
    holder: list[SolveResult] = []
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(m.cell_count + 10_000)
    try:
        threading.stack_size(512 * 1024 * 1024)
    except (ValueError, RuntimeError):
        threading.stack_size(64 * 1024 * 1024)
    t = threading.Thread(target=lambda: holder.append(_run_dfs_recursive(m)))
    t.start()
    t.join()
    threading.stack_size(0)
    sys.setrecursionlimit(old_limit)
    return holder[0]


def _run_dfs_recursive(m: Maze) -> SolveResult:
    t0 = time.perf_counter()
    cols, n = m.cols, m.cell_count
    parent = [-1] * n
    visited = [False] * n
    s = m.start[0] * cols + m.start[1]
    e = m.end[0] * cols + m.end[1]
    stats = {"count": 0, "depth": 0}

    def visit(cur: int, depth: int) -> bool:
        visited[cur] = True
        stats["count"] += 1
        if depth > stats["depth"]:
            stats["depth"] = depth
        if cur == e:
            return True
        for nb in _neighbors(m, cur):
            if not visited[nb]:
                parent[nb] = cur
                if visit(nb, depth + 1):
                    return True
        return False            # ngõ cụt -> quay lui

    found = visit(s, 1)
    path = _rebuild(parent, s, e, cols) if found else []
    return SolveResult("DFS (Đệ quy)", found, path, stats["count"], stats["depth"],
                       (time.perf_counter() - t0) * 1000, visited, cols)
