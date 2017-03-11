#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import socket
import random
import logging

from constants import MSG_DATE_SEP, END_MSG, ALLOWED_KEYS


logging.basicConfig(filename='jagger_client.log', level=logging.DEBUG)

logger = logging.getLogger("jagger_client")


def check_counter_and_skip(counter, skip_cicle=(1, 3)):
    """
    Check if counter is too big, if so then resets it accordingly to
    a equivalent value in the skip cicle.
    Then check if should ignore a this messages.
    This is done by getting the mod of counter by `den`,
    and then verifying if this number is lesser then `num - 1`.
    But for `counter == 0` it aways returns `True`.
    Ex:
        >>>check_counter_and_skip(counter=0, num=2, den=3)
        1, True
        >>>check_counter_and_skip(counter=1, num=2, den=3)
        2, True
        >>>check_counter_and_skip(counter=2, num=2, den=3)
        3, False
        >>>check_counter_and_skip(counter=3, num=2, den=3)
        4, True
        >>>check_counter_and_skip(counter=4, num=2, den=3)
        5, True
        >>>check_counter_and_skip(counter=5, num=2, den=3)
        6, False

    Return  a list containing:
        * The new checked counter(increased by one)
        * Boolean representing if has to ignore this counter or not
    """
    numerator, denominator = skip_cicle
    mod_counter = counter % denominator
    should_skip = mod_counter < numerator
    max_counter = 10000000
    if counter > max_counter:
        counter = mod_counter
    counter += 1
    return counter, should_skip


def prepare_msg(keys):
    now = datetime.datetime.utcnow().isoformat()
    str_keys = "".join(keys)
    msg = "%s%s%s" % (now, MSG_DATE_SEP, str_keys)
    return msg


def main_loop_controller(udp, dest, moves_proccessor, skip_cicle=(1, 3)):
    counter = 0
    while True:
        keys = moves_proccessor()
        msg = prepare_msg(keys)

        # should ignore a fragtion of the messages represented the skip cicle
        # also change the counter
        counter, should_skip = check_counter_and_skip(counter, skip_cicle)
        if should_skip:
            continue
        udp.sendto(msg.encode('UTF-8'), dest)


def default_moves_proccessor():
    num_active_pads = random.randint(0, 2)
    keys = random.sample(ALLOWED_KEYS, num_active_pads)
    return keys


def run(host, port=8765, moves_proccessor=default_moves_proccessor):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (host, port)
    try:
        main_loop_controller(udp, dest, moves_proccessor)
    except Exception as e:
        logger.exception(e)
    finally:
        udp.sendto(END_MSG.encode('UTF-8'), dest)
        udp.close()


if __name__ == '__main__':
    import sys
    host = sys.argv[1]
    # port = sys.args[2]
    run(host)
