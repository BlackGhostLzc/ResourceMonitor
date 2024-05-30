import curses
import psutil
from tabulate import tabulate

def draw_bar(win, y, x, color, value, totalValue, label):
    win.addstr(y, x, label)
    percent = int((value / totalValue) * 100)
    content = f"{percent}%"
    win.addstr(y + 1, x, content, curses.color_pair(color))
    blanks = (int)(30 * value / totalValue) - len(content)
    if blanks <= 0:
        return
    bar = ' '*blanks
    win.addstr(y + 1, x + len(content), bar, curses.color_pair(color))

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

disk_partions = [['C:\\', 'C:\\', 'NTFS', 'rw,fixed', 255, 260],
                 ['D:\\', 'D:\\', 'NTFS', 'rw,fixed', 255, 260]]
disk_usage = [214748360704, 179500625920, 35247734784, 83.6]
disk_io_counters = [695094, 608984, 18442267136, 44885284864, 376, 81]

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





