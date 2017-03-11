# -*- coding: utf-8 -*-
import keyboard

ALLOWED_KEYS = [
    'q',
    'e',
    's',
    'z',
    'c',
    '',
]


PRESSED_KEYS = set([
])


def initialize_keyboard():
    keyboard.press_and_release('esc')
    keyboard.press_and_release('esc')


def validate_keys(keys):
    valid_keys = []
    for key in keys:
        key = key.lower()
        if key not in ALLOWED_KEYS:
            return False
        valid_keys.append(key)

    return valid_keys


def prepare_release_keys_list(keys):
    released = []
    for key in PRESSED_KEYS:
        if key not in keys:
            released.append(key)
    return released


def prepare_new_keys_to_press(keys):
    new_keys = [k for k in keys if k not in PRESSED_KEYS]
    return new_keys


def press_keys(keys):
    global PRESSED_KEYS
    keys = validate_keys(keys)

    keys_to_release = prepare_release_keys_list(keys)
    if len(keys_to_release) != 0:
        print("releasing keys: %s" % keys_to_release)
        keyboard.release(",".join(keys_to_release))
        PRESSED_KEYS.difference_update(set(keys_to_release))

    new_keys = prepare_new_keys_to_press(keys)
    if len(new_keys) != 0 and '' not in new_keys:
        PRESSED_KEYS.update(keys)
        keys_to_press = ",".join(new_keys)
        print("pressing new: %s" % new_keys)
        keyboard.press(keys_to_press)
    print("current pressed keys: %s" % PRESSED_KEYS)
