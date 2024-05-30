import curses
import psutil

def display(data):
    curses.initscr()
    curses.curs_set(0)  # 隐藏光标

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # 蓝色边框
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # 绿色字体
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # 红色字体
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  #
    curses.init_pair(5, curses.COLOR_PAIRS, curses.COLOR_BLACK)  #
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)  #
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)  # 红色字体


    # userwin 的绘制
    user_win = curses.newwin(3, 40, 0, 0)
    user_win.attron(curses.color_pair(1))
    user_win.border(0)
    user_win.attroff(curses.color_pair(1))
    user_win.attron(curses.color_pair(7))
    user_win.addstr(0, 2, "user")
    user_win.attroff(curses.color_pair(7))
    user_win.addstr(1, 1, "{:.4f} seconds".format(data["cpu_times"].user))

    # sys_win 的绘制
    sys_win = curses.newwin(3, 40, 0, 40)
    sys_win.attron(curses.color_pair(1))
    sys_win.border(0)
    sys_win.attroff(curses.color_pair(1))
    sys_win.attron(curses.color_pair(7))
    sys_win.addstr(0, 2, "sys")
    sys_win.attroff(curses.color_pair(7))
    sys_win.addstr(1, 1, "{:.4f} seconds".format(data["cpu_times"].system))

    # idle 的绘制
    idle_win = curses.newwin(3, 40, 3, 0)
    idle_win.attron(curses.color_pair(1))
    idle_win.border(0)
    idle_win.attroff(curses.color_pair(1))
    idle_win.attron(curses.color_pair(7))
    idle_win.addstr(0, 2, "idle")
    idle_win.attroff(curses.color_pair(7))
    idle_win.addstr(1, 1, "{:.4f} seconds".format(data["cpu_times"].idle))

    # frequency 的绘制
    freq_win = curses.newwin(3, 40, 3, 40)
    freq_win.attron(curses.color_pair(1))
    freq_win.border(0)
    freq_win.attroff(curses.color_pair(1))
    freq_win.attron(curses.color_pair(7))
    freq_win.addstr(0, 2, "freq")
    freq_win.attroff(curses.color_pair(7))
    freq_win.addstr(1, 1, "{:.1f} MHz".format(data["cpu_freq"].current))


    # interrupt 个数的绘制
    interrupt_win = curses.newwin(3, 40, 6, 0)
    interrupt_win.attron(curses.color_pair(1))
    interrupt_win.border(0)
    interrupt_win.attroff(curses.color_pair(1))
    interrupt_win.attron(curses.color_pair(7))
    interrupt_win.addstr(0, 2, "interrupt")
    interrupt_win.attroff(curses.color_pair(7))
    interrupt_win.addstr(1, 1, "{} Number".format(data["cpu_stats"].interrupts))

    # syscall 个数的绘制
    syscall_win = curses.newwin(3, 40, 6, 40)
    syscall_win.attron(curses.color_pair(1))
    syscall_win.border(0)
    syscall_win.attroff(curses.color_pair(1))
    syscall_win.attron(curses.color_pair(7))
    syscall_win.addstr(0, 2, "syscall")
    syscall_win.attroff(curses.color_pair(7))
    syscall_win.addstr(1, 1, "{} Number".format(data["cpu_stats"].syscalls))

    # cpuwin 的绘制
    cpu_win = curses.newwin(6, 80, 9, 0)
    cpu_win.attron(curses.color_pair(1))
    cpu_win.border(0)
    cpu_win.attroff(curses.color_pair(1))
    cpu_win.attron(curses.color_pair(7))
    cpu_win.addstr(0, 2, "cpu")
    cpu_win.attroff(curses.color_pair(7))


    cpuCount = data["cpu_count"]

    blanks = int(80 / cpuCount)
    for i in range(cpuCount):
        cpu_win.vline(1, blanks * i, curses.ACS_VLINE, 1, curses.color_pair(1))
        cpu_win.vline(3, blanks * i, curses.ACS_VLINE, 1, curses.color_pair(1))

        cpu_win.addstr(1, blanks * i + 3, f"CPU {i}")
        cpu_win.addstr(3, blanks * i + 3, f"{cpu_percent[i]}%")


    cpu_win.hline(2, 1,  curses.ACS_HLINE, 80 - 2, curses.color_pair(1))


    user_win.refresh()
    idle_win.refresh()
    sys_win.refresh()
    freq_win.refresh()
    interrupt_win.refresh()
    syscall_win.refresh()
    cpu_win.refresh()


    # Wait for user input to exit
    cpu_win.getch()
    # Restore terminal to original state
    curses.endwin()


cpu_count = psutil.cpu_count()
cpu_percent = psutil.cpu_percent(percpu=True, interval=1)
cpu_times = psutil.cpu_times()
cpu_freq = psutil.cpu_freq()
cpu_stats = psutil.cpu_stats()

data = {
    "cpu_count": cpu_count,
    "cpu_percent": cpu_percent,
    "cpu_times": cpu_times,
    "cpu_freq": cpu_freq,
    "cpu_stats": cpu_stats,
}

print(cpu_times)
print(cpu_freq)
print(cpu_stats)

display(data)