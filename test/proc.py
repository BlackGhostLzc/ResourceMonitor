import psutil
import time
import curses
from tabulate import tabulate

def get_top_cpu_processes(n=5, interval=1):
    # 获取所有进程的列表
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # 初次调用cpu_percent以初始化
    for proc in processes:
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # 等待一段时间再获取CPU使用率
    # time.sleep(interval)

    # 获取CPU使用率
    processes_with_cpu = []
    for proc in processes:
        try:
            cpu_percent = proc.cpu_percent(interval=None)
            processes_with_cpu.append((proc, cpu_percent))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # 按CPU使用率排序并选择前n个进程
    top_processes = sorted(processes_with_cpu, key=lambda p: p[1], reverse=True)[:n]

    data = []
    for proc, cpu_percent in top_processes:
        data.append(proc.pid)
        data.append(proc.name())
        data.append(cpu_percent)

    return data

def curseInit():
    curses.initscr()
    curses.curs_set(0)  # 隐藏光标

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # 蓝色边框
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # 绿色字体
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # 红色字体
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  #
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)  #
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)  #
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)  # 红色字体
    # 填充
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_MAGENTA)  # Used
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_CYAN)  # Available
    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Free
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_BLUE)  # Cached


if __name__ == "__main__":
    data = get_top_cpu_processes(5)
    print(data)

    curseInit()
    proc_usage_win = curses.newwin(20, 70, 0, 0)

    proc_usage_win.attron(curses.color_pair(1))
    proc_usage_win.border(0)
    proc_usage_win.attroff(curses.color_pair(1))

    proc_usage_win.addstr(0, 2, "proc list")
    proc_usage_win.addstr(1, 2, "total process number 5")

    procNum = 5
    proc_usage_win.addstr(3, 2, f"top {procNum} process")

    proc_table = []
    proc_table.insert(0, ["pid", "name", "cpu"])
    for i in range(5):
        percent = f"{data[i*3 + 2]:.2f}%"
        proc_table.append([data[i*3], data[i*3 + 1], percent])

    table = tabulate(proc_table, headers="firstrow", tablefmt="grid")
    lines = table.split('\n')
    for i, line in enumerate(lines):
        if i == 0 or i == 1 or i == 2:
            proc_usage_win.addstr(i + 4, 1, line, curses.color_pair(3))
            continue
        if i >= 2:
            proc_usage_win.addstr(i + 4, 1, line, curses.color_pair(i % 7 + 1))

    proc_usage_win.refresh()
    proc_usage_win.getch()