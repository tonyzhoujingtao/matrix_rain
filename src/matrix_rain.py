#!/usr/bin/env python

import random
import curses


class Stream:
    def __init__(self, max_y, max_x, occupied_x):
        self.max_y = max_y
        self.max_x = max_x
        self.occupied_x = occupied_x
        self.reset(start_immediately=True)

    def reset(self, start_immediately=False):
        while True:
            self.x = random.randrange(0, self.max_x)
            if not any(
                occupied_x - 2 <= self.x <= occupied_x + 2
                for occupied_x in self.occupied_x
            ):
                self.occupied_x.add(self.x)
                break
        self.y = -random.randrange(0, self.max_y) if start_immediately else -self.length
        self.length = random.randrange(20, 50)
        self.speed = random.uniform(0.10, 2.0)

    def update(self, stdscr):
        self.chars = ["1", "0"] + random.choices(
            "abcdefghijklmnopqrstuvwxyz1234567890アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヰヱヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ",
            k=self.length,
        )

        for i in range(0, len(self.chars)):
            try:
                if self.y - i > 0:
                    color_pair = 1 if i < 5 else 2 if i < 10 else 3 if i < 15 else 4
                    stdscr.addstr(
                        int(self.y) - i,
                        self.x,
                        self.chars[i],
                        curses.color_pair(color_pair),
                    )
            except curses.error:
                pass

        self.y += self.speed

        if self.y > self.max_y + self.length:
            self.occupied_x.remove(self.x)
            self.reset()


def main(stdscr):
    if curses.can_change_color():
        curses.init_color(1, 1000, 1000, 1000)
        curses.init_color(2, 500, 1000, 500)
        curses.init_color(3, 0, 1000, 0)
        curses.init_color(4, 0, 500, 0)

        for i in range(1, 5):
            curses.init_pair(i, i, curses.COLOR_BLACK)

    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    curses.start_color()

    while True:
        max_y, max_x = stdscr.getmaxyx()
        occupied_x = set()
        streams = [Stream(max_y, max_x, occupied_x) for _ in range(int(0.2 * max_x))]

        while True:
            stdscr.clear()

            for stream in streams:
                stream.update(stdscr)

            while len(streams) < 0.2 * max_x:
                streams.append(Stream(max_y, max_x, occupied_x))

            stdscr.refresh()

            new_max_y, new_max_x = stdscr.getmaxyx()
            if new_max_y != max_y or new_max_x != max_x:
                break

            ch = stdscr.getch()
            if ch == ord("q"):
                return


if __name__ == "__main__":
    curses.wrapper(main)
