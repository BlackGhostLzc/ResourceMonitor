import curses
import time


def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Turn off cursor
    curses.curs_set(0)

    # Set the timeout for getch (non-blocking input check)
    stdscr.timeout(1000)  # 1000 ms = 1 second

    counter = 0

    while True:
        # Clear the screen
        stdscr.clear()

        # Display the counter
        stdscr.addstr(0, 0, f"Counter: {counter}")

        # Refresh the screen to update content
        stdscr.refresh()

        # Wait for user input (non-blocking)
        key = stdscr.getch()

        # Exit on 'q' key press
        if key == ord('q'):
            break

        # Increment the counter
        counter += 1

        # Sleep for a short duration to slow down the loop
        time.sleep(1)


if __name__ == "__main__":
    curses.wrapper(main)