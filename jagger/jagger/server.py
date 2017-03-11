#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import socket
import logging

import dateutil.parser

from constants import MSG_DATE_SEP, END_MSG
# from moves import initialize_keyboard, press_keys

logging.basicConfig(filename='jagger_server.log', level=logging.DEBUG)
logger = logging.getLogger("jagger_server")


class JaggerServer(object):
    def __init__(self, host, port=8765):
        super(JaggerServer, self).__init__()
        self.host = host
        self.port = port

        self.total_msgs = 0
        self.total_delay = 0
        self.avg_delay = 0
        self.max_delay = 0
        self.min_delay = 1000000000
        self.max_msg_count = 1000

    def get_msg(self, client_msg):
        if MSG_DATE_SEP in client_msg:
            client_time, msg = client_msg.split(MSG_DATE_SEP)

            client_time = dateutil.parser.parse(client_time)

            return client_time, msg
        else:
            pass

    def proccess_msg(self, client_msg):
        now = datetime.datetime.utcnow()
        client_time, msg = self.get_msg(client_msg)
        time_delay = now - client_time
        # time delay in miliseconds
        time_delay = time_delay.total_seconds() * 1000

        keys = [key for key in msg]
        # logger.debug("pressed keys: %s" % keys
        # press_keys(keys)
        return time_delay

    def calculate_stats_on_delay(self, time_delay):

        self.min_delay = min(self.min_delay, time_delay)
        self.max_delay = max(self.max_delay, time_delay)
        self.total_delay += time_delay
        self.total_msgs += 1

        # calculate the avg once the max msg count is archived
        if self.total_msgs >= self.max_msg_count:
            new_avg = self.total_delay / self.total_msgs
            self.avg_delay = (self.avg_delay + new_avg) / 2
            self.total_delay = 0
            self.total_msgs = 0
        logger.debug("Delay: current: {} min: {} max: {} avg: {}".format(
            time_delay,
            self.min_delay,
            self.max_delay,
            self.avg_delay
        ))

    def main_loop_controller(self, udp):
        while True:
            client_msg_binary, client = udp.recvfrom(1024)
            client_msg = client_msg_binary.decode('UTF-8')
            if END_MSG in client_msg:
                break
            time_delay = self.proccess_msg(client_msg)
            self.calculate_stats_on_delay(time_delay)

    def run(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        orig = (self.host, self.port)
        udp.bind(orig)
        # initialize_keyboard()
        try:
            self.main_loop_controller(udp)
        except Exception as e:
            logger.exception(e)
        finally:
            logger.debug("close")
            udp.close()


if __name__ == '__main__':
    server = JaggerServer(host='', port=8765)
    server.run()
