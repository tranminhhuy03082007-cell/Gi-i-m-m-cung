"""Maze Solver - BFS vs DFS (CLI). Chạy: python main.py"""
import io
import sys
import benchmark
import generator
import tests
import view
from maze import Maze
from solvers import bfs, dfs_iterative, dfs_recursive

DEMO = [
    "#####################",
    "#S        #         #",
    "# ####### # ####### #",
    "# #     # #       # #",
    "# # ### # ######### #",
    "# # # #             #",
    "# # # # ########### #",
    "#   #   #         # #",
    "##### ### ####### # #",
    "#     #         #   #",
    "# ##### ##### # #####",
    "#       #     #    E#",
    "#####################",
]


def read_int(prompt: str, default: int) -> int:
    s = input(f"{prompt} [{default}]: ").strip()
    return int(s) if s.isdigit() and int(s) > 0 else default


def compare(b, d) -> None:
    """Phân tích tự động sự khác biệt giữa đường đi của BFS và DFS."""
    print("\n--- PHÂN TÍCH BFS vs DFS ---")
    if not b.found:
        print("  Không có đường đi: cả hai đều duyệt hết vùng liên thông chứa S rồi kết luận vô nghiệm.")
        return
    print(f"  Độ dài đường đi : BFS = {b.path_length}  |  DFS = {d.path_length}")
    print(f"  Số ô đã duyệt   : BFS = {b.visited_count}  |  DFS = {d.visited_count}")
    print(f"  Peak frontier   : BFS = {b.peak_frontier}  |  DFS = {d.peak_frontier}")
    if d.path_length > b.path_length:
        print(f"  => DFS đi dài hơn {d.path_length - b.path_length} bước ({d.path_length / b.path_length:.2f} lần). "
              "BFS đảm bảo đường ngắn nhất.")
    else:
        print("  => Ở mê cung này DFS tình cờ cũng ra đường ngắn nhất (thường gặp khi chỉ có 1 đường duy nhất).")
    if d.visited_count < b.visited_count:
        print("  => DFS duyệt ít ô hơn vì 'đâm sâu' may mắn đúng hướng; BFS luôn loang đều theo mọi hướng.")
    else:
        print("  => DFS phải quay lui nhiều (ngõ cụt) nên duyệt không ít hơn BFS.")


def solve_and_show(m: Maze) -> None:
    print(f"\n=== {m.name}: {m.rows}x{m.cols} = {m.cell_count} ô ===")
    print("--- MÊ CUNG BAN ĐẦU ---")
    view.print_maze(m)
    b, d, rc = bfs(m), dfs_iterative(m), dfs_recursive(m)
    for r in (b, d):
        print(f"\n--- KẾT QUẢ: {r.algorithm} ---")
        view.print_maze(m, r, show_visited=True)
        view.print_stats(r)
    view.print_legend()
    view.print_stats(rc)
    compare(b, d)


def random_mode() -> None:
    rows, cols = read_int("Số hàng (lẻ)", 15), read_int("Số cột (lẻ)", 31)
    loop, seed = read_int("Tỉ lệ phá tường tạo nhiều đường đi (%)", 15), read_int("Seed", 7)
    solve_and_show(generator.generate(rows, cols, seed, loop / 100))


def file_mode() -> None:
    path = input("Đường dẫn file: ").strip().strip('"')
    try:
        solve_and_show(Maze.from_file(path))
    except (OSError, ValueError) as ex:
        print("Lỗi:", ex)


def main() -> None:
    # Ép console xuất UTF-8 (để hiển thị tiếng Việt và ký tự ██ trên Windows)
    stdout = sys.stdout
    if isinstance(stdout, io.TextIOWrapper):
        stdout.reconfigure(encoding="utf-8")
    actions = {
        "1": lambda: solve_and_show(Maze.from_lines(DEMO, "Mê cung mẫu 13x21")),
        "2": random_mode,
        "3": file_mode,
        "4": tests.run_all,
        "5": benchmark.run,
    }
    while True:
        print("\n=========== MAZE SOLVER (BFS vs DFS) ===========")
        print(" 1. Demo mê cung mẫu\n 2. Sinh mê cung ngẫu nhiên và giải\n 3. Đọc mê cung từ file văn bản")
        print(" 4. Chạy bộ test case (nhỏ + cận biên)\n 5. Benchmark hiệu năng (dữ liệu lớn)\n 0. Thoát")
        choice = input("Chọn: ").strip()
        if choice == "0":
            return
        actions.get(choice, lambda: print("Lựa chọn không hợp lệ."))()


if __name__ == "__main__":
    main()
