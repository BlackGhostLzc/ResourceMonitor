import curses

def display(stdscr):
    # 清除屏幕
    stdscr.clear()
    curses.curs_set(0)

    # 颜色对定义
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)  # Used
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)     # Available
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)   # Free
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)     # Cached

    # 数据
    total_memory = 15.50
    used_memory = 3.60
    available_memory = 10.70
    free_memory = 7.20
    cached_memory = 4.30

    # 绘制内存使用情况
    stdscr.addstr(0, 0, "Memory(RAM)", curses.A_BOLD)

    # 绘制条形图
    def draw_bar(y, label, value, color_pair):
        content = f"{label}G/{total_memory}G"
        stdscr.addstr(y, 1, content, curses.color_pair(color_pair))
        bar = ' ' * (30 - len(content))
        stdscr.addstr(y, 1 + len(content), bar, curses.color_pair(color_pair))

    draw_bar(2, "Used: ", used_memory, 1)
    draw_bar(4, "Available: ", available_memory, 2)
    draw_bar(6, "Free: ", free_memory, 3)
    draw_bar(8, "Cached: ", cached_memory, 4)

    # 刷新屏幕
    stdscr.refresh()

    # 等待用户输入以退出
    stdscr.getch()

curses.wrapper(display)
