#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constants import ALLOWED_KEYS
from client import run
import keyboard


def key_press_moves_processor():
    keys = [key for key in ALLOWED_KEYS[:-1] if keyboard.is_pressed(key)]
    return keys


if __name__ == '__main__':
    import sys
    host = sys.argv[1]
    port = 8865
    run(host, port, moves_proccessor=key_press_moves_processor)
