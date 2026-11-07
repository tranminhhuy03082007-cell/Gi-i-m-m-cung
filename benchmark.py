"""Đo thời gian (perf_counter) và bộ nhớ đỉnh (tracemalloc) của BFS / DFS; xuất CSV + biểu đồ ASCII."""
import csv
import gc
import tracemalloc
import generator
from solvers import bfs, dfs_iterative, dfs_recursive

ALGOS = (("BFS", bfs), ("DFS-Stack", dfs_iterative), ("DFS-Đệ quy", dfs_recursive))


def _measure(m, solver, repeats):
    solver(m)  # warm-up
    gc.collect()
    times = [solver(m).elapsed_ms for _ in range(repeats)]  # đo thời gian khi KHÔNG bật tracemalloc
    if solver is dfs_recursive and m.cell_count > 100_000:
        # tracemalloc + đệ quy sâu (hàng chục nghìn khung) chậm bất thường -> bỏ đo bộ nhớ ca này
        res, peak = solver(m), float("nan")
    else:
        tracemalloc.start()
        res = solver(m)
        peak = tracemalloc.get_traced_memory()[1]           # đo bộ nhớ ở lần chạy riêng
        tracemalloc.stop()
    return dict(case=m.name, cells=m.cell_count, algo="", found=res.found, path_len=res.path_length,
                visited=res.visited_count, peak_frontier=res.peak_frontier,
                time_ms=sum(times) / len(times), mem_kb=peak / 1024)


def run(repeats: int = 3, sizes=(21, 101, 201, 301, 501)) -> None:
    print(f"\n===== BENCHMARK (thời gian = trung bình {repeats} lần chạy) =====")
    mazes = []
    for n in sizes:
        p = generator.generate(n, n, 1, 0);    p.name = f"Perfect {n}x{n}"
        b = generator.generate(n, n, 1, 0.15); b.name = f"Braid15% {n}x{n}"
        mazes += [p, b, generator.open_field(n, n)]

    rows = []
    for m in mazes:
        for name, fn in ALGOS:
            row = _measure(m, fn, repeats)
            row["algo"] = name
            rows.append(row)
            print(f"  ... {m.name} / {name} xong", end="\r")

    print(" " * 60)
    print(f"{'Mê cung':<22}{'Số ô':>9} {'Thuật toán':<11}{'Độ dài':>8}{'Đã duyệt':>10}{'Peak':>9}{'Time(ms)':>11}{'Mem(KB)':>11}")
    print("-" * 93)
    prev = None
    for r in rows:
        if prev and prev != r["case"]:
            print()
        prev = r["case"]
        pl = r["path_len"] if r["found"] else "-"
        print(f"{r['case']:<22}{r['cells']:>9} {r['algo']:<11}{pl:>8}{r['visited']:>10}"
              f"{r['peak_frontier']:>9}{r['time_ms']:>11.3f}{('n/a' if r['mem_kb'] != r['mem_kb'] else format(r['mem_kb'], '.1f')):>11}")

    sel = [r for r in rows if r["case"].endswith("301x301")]
    if sel:
        print("\n--- Biểu đồ thời gian (ms) - các mê cung 301x301 ---")
        mx = max(r["time_ms"] for r in sel) or 1
        for r in sel:
            print(f"{r['case']:<20}{r['algo']:<11}|{'█' * max(1, round(r['time_ms'] / mx * 50))} {r['time_ms']:.3f}")

    with open("benchmark_results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("\nĐã xuất benchmark_results.csv (mở bằng Excel để vẽ biểu đồ cho báo cáo).")
