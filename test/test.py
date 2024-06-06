import curses

def main(stdscr):
    curses.curs_set(0)  # 隐藏光标

    # 获取标准屏幕窗口的大小
    height, width = stdscr.getmaxyx()
    print(height)
    print(width)


curses.wrapper(main)
