import curses

def main(stdscr):
    # 初始化
    curses.curs_set(0)  # 隐藏光标
    stdscr.clear()      # 清空屏幕
    stdscr.refresh()    # 刷新屏幕

    # 检查是否支持颜色
    if not curses.has_colors():
        raise RuntimeError("Terminal does not support colors")

    # 启用颜色
    curses.start_color()

    # 定义颜色对
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)   # 蓝色边框
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # 绿色字体
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    # 红色字体

    # 获取屏幕尺寸
    height, width = stdscr.getmaxyx()

    # 创建窗口
    win = curses.newwin(height // 2, width // 2, height // 4, width // 4)

    # 绘制边框
    win.attron(curses.color_pair(1))  # 使用蓝色
    win.border(0)

    # 设置文本颜色
    win.attron(curses.color_pair(2))  # 使用绿色
    # 在窗口中心写入文本
    win.addstr(height // 4, width // 4, "Hello, World!")


    # 设置边框颜色
    win.attron(curses.color_pair(1))  # 使用蓝色
    # 绘制窗口标题
    win.addstr(0, 1, "Custom Window")

    # 刷新窗口
    win.refresh()

    # 等待用户输入
    stdscr.getch()

# 运行主程序
if __name__ == "__main__":
    curses.wrapper(main)