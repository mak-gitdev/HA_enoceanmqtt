# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import
import logging
import socket
import time


from enocean.communicators.communicator import Communicator


class TCPClientCommunicator(Communicator):
    ''' Socket communicator class for EnOcean radio '''
    logger = logging.getLogger('enocean.communicators.TCPClientCommunicator')

    def __init__(self, host='', port=9637):
        super(TCPClientCommunicator, self).__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.logger.info('TCPClientCommunicator started')
        self.sock.settimeout(0.5)
        try:
            self.sock.connect(( self.host, self.port))
        except socket.error as e:
            self.logger.error('Exception occured while connecting: ' + str(e))
            self.stop()

        while not self._stop_flag.is_set():
            # If there's messages in transmit queue
            # send them
            while True:
                packet = self._get_from_send_queue()
                if not packet:
                    break
                try:
                    self.sock.send(bytearray(packet.build()))
                except Exception as e:
                    self.logger.error('Exception occured while sending: ' + str(e))
                    self.stop()

            try:
                self._buffer.extend(bytearray(self.sock.recv(16)))
                self.parse()
            except socket.timeout:
                time.sleep(0)
            except Exception as e:
                self.logger.error('Exception occured while parsing: ' + str(e))
            time.sleep(0)

        self.sock.close()
        self.logger.info('TCPClientCommunicator stopped')
