import curses
from tabulate import tabulate

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


def displayLs(list):
    pass


def displayCpuInfo(data):
    curseInit()

    # userwin 的绘制
    user_win = curses.newwin(3, 40, 0, 0)
    user_win.attron(curses.color_pair(1))
    user_win.border(0)
    user_win.attroff(curses.color_pair(1))
    user_win.attron(curses.color_pair(7))
    user_win.addstr(0, 2, "user")
    user_win.attroff(curses.color_pair(7))
    user_win.addstr(1, 1, "{:.4f} seconds".format(data["cpu_times"][0]))

    # sys_win 的绘制
    sys_win = curses.newwin(3, 40, 0, 40)
    sys_win.attron(curses.color_pair(1))
    sys_win.border(0)
    sys_win.attroff(curses.color_pair(1))
    sys_win.attron(curses.color_pair(7))
    sys_win.addstr(0, 2, "sys")
    sys_win.attroff(curses.color_pair(7))
    sys_win.addstr(1, 1, "{:.4f} seconds".format(data["cpu_times"][1]))

    # idle 的绘制
    idle_win = curses.newwin(3, 40, 3, 0)
    idle_win.attron(curses.color_pair(1))
    idle_win.border(0)
    idle_win.attroff(curses.color_pair(1))
    idle_win.attron(curses.color_pair(7))
    idle_win.addstr(0, 2, "idle")
    idle_win.attroff(curses.color_pair(7))
    idle_win.addstr(1, 1, "{:.4f} seconds".format(data["cpu_times"][2]))

    # frequency 的绘制
    freq_win = curses.newwin(3, 40, 3, 40)
    freq_win.attron(curses.color_pair(1))
    freq_win.border(0)
    freq_win.attroff(curses.color_pair(1))
    freq_win.attron(curses.color_pair(7))
    freq_win.addstr(0, 2, "freq")
    freq_win.attroff(curses.color_pair(7))
    freq_win.addstr(1, 1, "{:.1f} MHz".format(data["cpu_freq"][0]))

    # interrupt 个数的绘制
    interrupt_win = curses.newwin(3, 40, 6, 0)
    interrupt_win.attron(curses.color_pair(1))
    interrupt_win.border(0)
    interrupt_win.attroff(curses.color_pair(1))
    interrupt_win.attron(curses.color_pair(7))
    interrupt_win.addstr(0, 2, "interrupt")
    interrupt_win.attroff(curses.color_pair(7))
    interrupt_win.addstr(1, 1, "{} Number".format(data["cpu_stats"][1]))

    # syscall 个数的绘制
    syscall_win = curses.newwin(3, 40, 6, 40)
    syscall_win.attron(curses.color_pair(1))
    syscall_win.border(0)
    syscall_win.attroff(curses.color_pair(1))
    syscall_win.attron(curses.color_pair(7))
    syscall_win.addstr(0, 2, "syscall")
    syscall_win.attroff(curses.color_pair(7))
    syscall_win.addstr(1, 1, "{} Number".format(data["cpu_stats"][3]))

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
    cpu_percent = data["cpu_percent"]

    for i in range(cpuCount):
        cpu_win.vline(1, blanks * i, curses.ACS_VLINE, 1, curses.color_pair(1))
        cpu_win.vline(3, blanks * i, curses.ACS_VLINE, 1, curses.color_pair(1))

        cpu_win.addstr(1, blanks * i + 3, f"CPU {i}")
        cpu_win.addstr(3, blanks * i + 3, f"{cpu_percent[i]}%")

    cpu_win.hline(2, 1, curses.ACS_HLINE, 80 - 2, curses.color_pair(1))

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

    # Wait for user input to exit
    cpu_win.getch()
    # Restore terminal to original state
    curses.endwin()



def displayMemInfo(data):
    virtual_mem_total = data["virtual_mem"][0] / (1024 ** 3)
    virtual_mem_available = data["virtual_mem"][1] / (1024 ** 3)
    virtual_mem_used = data["virtual_mem"][3] / (1024 ** 3)
    virtual_mem_free = data["virtual_mem"][4] / (1024 ** 3)
    virtual_mem_used_percent = data["virtual_mem"][2]

    swap_mem_total = data["swap_mem"][0] / (1024 ** 3)
    swap_mem_used = data["swap_mem"][1] / (1024 ** 3)
    swap_mem_free = data["swap_mem"][2] / (1024 ** 3)
    swap_mem_used_percent = data["swap_mem"][3]

    curseInit()

    virtual_win = curses.newwin(15, 30, 0, 0)
    swap_win = curses.newwin(15, 30, 0, 30)

    virtual_win.attron(curses.color_pair(1))
    virtual_win.border(0)
    virtual_win.attroff(curses.color_pair(1))

    swap_win.attron(curses.color_pair(1))
    swap_win.border(0)
    swap_win.attroff(curses.color_pair(1))

    virtual_win.addstr(0, 2, "vmem")
    swap_win.addstr(0, 2, "smem")

    virtual_win.attron(curses.color_pair(4))
    virtual_win.addstr(1, 1, "total: {:.4f} GB".format(virtual_mem_total))
    virtual_win.attroff(curses.color_pair(4))

    swap_win.attron(curses.color_pair(4))
    swap_win.addstr(1, 1, "total: {:.4f} GB".format(swap_mem_total))
    swap_win.attroff(curses.color_pair(4))

    draw_bar(virtual_win, 3, 1, 10, virtual_mem_used, virtual_mem_total, "used:")
    draw_bar(virtual_win, 6, 1, 11, virtual_mem_available, virtual_mem_total, "available:")
    draw_bar(virtual_win, 9, 1, 9, virtual_mem_free, virtual_mem_total, "free:")

    draw_bar(swap_win, 3, 1, 10, swap_mem_used, swap_mem_total, "used:")
    draw_bar(swap_win, 6, 1, 11, swap_mem_free, swap_mem_total, "free:")

    virtual_win.refresh()
    swap_win.refresh()

    swap_win.getch()
    curses.endwin()


def displayDiskInfo(diskInfo):
    # 这是一个二维列表
    # device, mountpoint, fstype, opts, maxfile, maxpath
    disk_partions = diskInfo["disk_partions"]
    # 一维列表
    # total, used, free, percent
    disk_usage = diskInfo["disk_usage"]
    # 一维列表
    # read_count, write_count, read_bytes, write_bytes, read_time, write_time
    disk_io_counters = diskInfo["disk_io_counters"]
    curseInit()


    disk_usage_win = curses.newwin(10, 35, 0, 0)

    disk_usage_win.attron(curses.color_pair(1))
    disk_usage_win.border(0)
    disk_usage_win.attroff(curses.color_pair(1))

    disk_usage_win.addstr(0, 2, "disk-usage")

    totalSz = disk_usage[0] / (1024 ** 3)
    usedSz = disk_usage[1] / (1024 ** 3)
    freeSz = disk_usage[2] / (1024 ** 3)

    disk_usage_win.attron(curses.color_pair(2))
    disk_usage_win.addstr(1, 1, "total: {:.2f}GB".format(totalSz))
    disk_usage_win.attroff(curses.color_pair(2))

    draw_bar(disk_usage_win, 2, 1, 10, usedSz, totalSz, "used:")
    draw_bar(disk_usage_win, 5, 1, 11, freeSz, totalSz, "free:")

    # 绘制diskio
    disk_io_win = curses.newwin(10, 35, 0, 35)
    disk_io_win.attron(curses.color_pair(1))
    disk_io_win.border(0)
    disk_io_win.attroff(curses.color_pair(1))
    disk_io_win.addstr(0, 2, "disk-io")

    disk_io_win.addstr(1, 1, f"read_count:  {disk_io_counters[0]}", curses.color_pair(2))
    disk_io_win.addstr(2, 1, f"write_count: {disk_io_counters[1]}", curses.color_pair(3))
    disk_io_win.addstr(3, 1, f"read_bytes:  {disk_io_counters[2]}", curses.color_pair(4))
    disk_io_win.addstr(4, 1, f"write_bytes: {disk_io_counters[3]}", curses.color_pair(1))
    disk_io_win.addstr(5, 1, f"read_time:   {disk_io_counters[4]}", curses.color_pair(6))
    disk_io_win.addstr(6, 1, f"write_time:  {disk_io_counters[5]}", curses.color_pair(7))

    # 绘制表格
    disk_part_win = curses.newwin(7 + len(disk_partions), 78, 10, 0)

    disk_part_win.attron(curses.color_pair(1))
    disk_part_win.border(0)
    disk_part_win.attroff(curses.color_pair(1))

    disk_part_win.addstr(0, 2, "disk-partions")

    tableCol = ["device", "mountpoint", "fstype", "opts", "maxfile", "maxpath"]
    disk_partions.insert(0, tableCol)
    table = tabulate(disk_partions, headers="firstrow", tablefmt="grid")
    lines = table.split('\n')
    for i, line in enumerate(lines):
        if i == 0 or i == 1 or i == 2:
            disk_part_win.addstr(i + 1, 1, line, curses.color_pair(3))
            continue
        if i >= 2:
            disk_part_win.addstr(i + 1, 1, line, curses.color_pair(i % 7 + 1))

    disk_usage_win.refresh()
    disk_io_win.refresh()
    disk_part_win.refresh()
    disk_usage_win.getch()
    curses.endwin()



def draw_bar(win, y, x, color, value, totalValue, label):
    win.addstr(y, x, label)
    percent = int((value / totalValue) * 100)
    content = f"{percent}%"
    win.addstr(y + 1, x, content, curses.color_pair(color))
    blanks = (int)(30 * value / totalValue) - len(content)
    if blanks <= 0:
        return
    bar = ' ' * blanks
    win.addstr(y + 1, x + len(content), bar, curses.color_pair(color))







