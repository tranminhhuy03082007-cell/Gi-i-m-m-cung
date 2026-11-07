"""Biểu diễn mê cung bằng ma trận 2D và cấu trúc kết quả."""
from __future__ import annotations
from dataclasses import dataclass, field

# Mã các loại ô trong ma trận
PATH, WALL, START, END = 0, 1, 2, 3

Point = tuple[int, int]  # (hàng, cột)


class Maze:
    """Mê cung = list[list[int]]. Văn bản: '#'/'1' tường, 'S' bắt đầu, 'E' kết thúc, còn lại là đường đi."""

    def __init__(self, grid: list[list[int]], start: Point, end: Point, name: str = ""):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.start = start
        self.end = end
        self.name = name

    @property
    def cell_count(self) -> int:
        return self.rows * self.cols

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_walkable(self, r: int, c: int) -> bool:
        return self.in_bounds(r, c) and self.grid[r][c] != WALL

    @staticmethod
    def from_lines(lines: list[str], name: str = "") -> "Maze":
        if not lines:
            raise ValueError("Mê cung rỗng.")
        rows, cols = len(lines), max(len(l) for l in lines)
        grid = [[PATH] * cols for _ in range(rows)]
        start = end = None
        for r in range(rows):
            for c in range(cols):
                ch = lines[r][c].upper() if c < len(lines[r]) else "#"
                if ch in "#1":
                    grid[r][c] = WALL
                elif ch == "S":
                    grid[r][c], start = START, (r, c)
                elif ch == "E":
                    grid[r][c], end = END, (r, c)
        if start is None:
            raise ValueError("Mê cung thiếu điểm bắt đầu 'S'.")
        if end is None:
            raise ValueError("Mê cung thiếu điểm kết thúc 'E'.")
        return Maze(grid, start, end, name)

    @staticmethod
    def from_file(path: str) -> "Maze":
        with open(path, encoding="utf-8") as f:
            return Maze.from_lines(f.read().splitlines(), path)

    def save(self, path: str) -> None:
        sym = {WALL: "#", START: "S", END: "E", PATH: " "}
        with open(path, "w", encoding="utf-8") as f:
            for row in self.grid:
                f.write("".join(sym[v] for v in row) + "\n")


@dataclass
class SolveResult:
    algorithm: str
    found: bool
    path: list[Point] = field(default_factory=list)
    visited_count: int = 0      # số ô đã duyệt
    peak_frontier: int = 0      # kích thước lớn nhất của Queue/Stack/độ sâu đệ quy
    elapsed_ms: float = 0.0
    visited: list[bool] = field(default_factory=list)  # phẳng, chỉ số r*cols+c
    cols: int = 0

    @property
    def path_length(self) -> int:
        """Số bước đi; -1 nếu không có đường."""
        return len(self.path) - 1 if self.found else -1

    def is_visited(self, r: int, c: int) -> bool:
        return self.visited[r * self.cols + c]
