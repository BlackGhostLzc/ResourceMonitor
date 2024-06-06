import curses

def display():
    virtual_mem_total = 15.74
    virtual_mem_available = 12.30
    virtual_mem_used = 3.00
    virtual_mem_free = 1.02
    virtual_mem_used_percent = 25

    swap_mem_total = 5.89
    swap_mem_used = 1.89
    swap_mem_free = 3.83
    swap_mem_used_percent = 67

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

    # 填充
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_MAGENTA)  # Used
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_CYAN)  # Available
    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Free
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_BLUE)  # Cached

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

    virtual_win.getch()

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


display()




