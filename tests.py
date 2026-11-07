"""Bộ test case nhỏ + cận biên, tự kiểm tra tính hợp lệ của đường đi."""
from maze import Maze
from solvers import bfs, dfs_iterative, dfs_recursive
import generator

CASES = [
    ("Nhỏ - có đường", ["#######", "#S    #", "# ### #", "#   #E#", "#######"], True, None),
    ("Cận biên - S kề E", ["####", "#SE#", "####"], True, 1),
    ("Cận biên - hành lang 1 hàng (không tường biên)", ["S   E"], True, 4),
    ("Cận biên - KHÔNG có đường", ["#######", "#S # E#", "#  #  #", "#######"], False, None),
    ("Hai lối: ngắn (4) & dài (12) - DFS đi vòng",
     ["#######", "#S    #", "# ### #", "#     #", "# ### #", "#E    #", "#######"], True, 4),
    ("Phòng trống 4x5", ["#######", "#S    #", "#     #", "#     #", "#    E#", "#######"], True, 7),
]


def is_valid_path(m: Maze, path) -> bool:
    """Bắt đầu tại S, kết thúc tại E, ô liên tiếp kề nhau, không đi qua tường."""
    if not path or path[0] != m.start or path[-1] != m.end:
        return False
    for i, (r, c) in enumerate(path):
        if not m.is_walkable(r, c):
            return False
        if i and abs(r - path[i - 1][0]) + abs(c - path[i - 1][1]) != 1:
            return False
    return True


def run_all() -> bool:
    print("\n===== CHẠY BỘ TEST CASE =====")
    passed = total = 0

    for name, lines, expect_found, expect_len in CASES:
        total += 1
        m = Maze.from_lines(lines, name)
        b, d, rc = bfs(m), dfs_iterative(m), dfs_recursive(m)
        ok = b.found == d.found == rc.found == expect_found
        if ok and expect_found:
            ok = (is_valid_path(m, b.path) and is_valid_path(m, d.path) and is_valid_path(m, rc.path)
                  and b.path_length <= d.path_length          # BFS luôn ngắn nhất
                  and d.path_length == rc.path_length          # 2 bản DFS cùng thứ tự duyệt
                  and (expect_len is None or b.path_length == expect_len))
        passed += ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: BFS={b.path_length}, DFS={d.path_length}, DFS-đệ quy={rc.path_length}")

    total += 1
    try:
        Maze.from_lines(["###", "#S#", "###"])
        print("  [FAIL] Thiếu E không báo lỗi")
    except ValueError:
        passed += 1
        print("  [PASS] Cận biên - thiếu điểm E -> báo lỗi đúng")

    total += 1
    ok = True
    for seed in range(1, 21):
        m = generator.generate(41, 41, seed, 0.2)
        b, d = bfs(m), dfs_iterative(m)
        ok &= b.found and d.found and is_valid_path(m, b.path) and is_valid_path(m, d.path) and b.path_length <= d.path_length
    passed += ok
    print(f"  [{'PASS' if ok else 'FAIL'}] 20 mê cung ngẫu nhiên 41x41 (loop 20%): BFS <= DFS & đường hợp lệ")

    print(f"\n  Kết quả: {passed}/{total} test đạt.")
    return passed == total
