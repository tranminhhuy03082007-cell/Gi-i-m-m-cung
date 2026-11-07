"""Hiển thị mê cung trên console bằng mã màu ANSI."""
from maze import Maze, SolveResult, WALL, START, END

MAX_ROWS, MAX_COLS = 40, 70
RESET = "\033[0m"
GRAY, GREEN, RED, YELLOW, CYAN = "\033[90m", "\033[92m", "\033[91m", "\033[93m", "\033[96m"


def print_maze(m: Maze, result: SolveResult | None = None, show_visited: bool = False) -> None:
    if m.rows > MAX_ROWS or m.cols > MAX_COLS:
        print(f"  (Mê cung {m.rows}x{m.cols} quá lớn để hiển thị - bỏ qua phần vẽ)")
        return
    on_path = set(result.path) if result and result.found else set()
    for r in range(m.rows):
        line = ["  "]
        for c in range(m.cols):
            v = m.grid[r][c]
            if v == WALL:
                line.append(f"{GRAY}██{RESET}")
            elif v == START:
                line.append(f"{GREEN}S {RESET}")
            elif v == END:
                line.append(f"{RED}E {RESET}")
            elif (r, c) in on_path:
                line.append(f"{YELLOW}* {RESET}")
            elif show_visited and result and result.is_visited(r, c):
                line.append(f"{CYAN}. {RESET}")
            else:
                line.append("  ")
        print("".join(line))


def print_legend() -> None:
    print("  Chú thích: ██ tường | S bắt đầu | E kết thúc | * đường đi | . ô đã duyệt")


def print_stats(r: SolveResult) -> None:
    length = r.path_length if r.found else "-"
    print(f"  [{r.algorithm}] Tìm thấy: {'CÓ' if r.found else 'KHÔNG'} | Độ dài: {length} bước | "
          f"Ô đã duyệt: {r.visited_count} | Peak frontier: {r.peak_frontier} | Thời gian: {r.elapsed_ms:.3f} ms")
