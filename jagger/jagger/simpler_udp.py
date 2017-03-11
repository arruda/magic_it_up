#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import socket
import logging

import dateutil.parser

logging.basicConfig(filename='simple_udp.log', level=logging.DEBUG)
logger = logging.getLogger("simple_udp")

host = ''
port = 8765
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (host, port)
udp.bind(orig)
# initialize_keyboard()
try:

    while True:
        client_msg_binary, client = udp.recvfrom(1024)
        client_msg = client_msg_binary.decode('UTF-8')

        client_time, msg = client_msg.split('>>>:')

        client_time = dateutil.parser.parse(client_time)

        now = datetime.datetime.utcnow()
        client_time, msg = client_msg
        time_delay = now - client_time
        # time delay in miliseconds
        time_delay = time_delay.total_seconds() * 1000
        logger.debug(time_delay)
except Exception as e:
    logger.exception(e)
finally:
    logger.debug("close")
    udp.close()
