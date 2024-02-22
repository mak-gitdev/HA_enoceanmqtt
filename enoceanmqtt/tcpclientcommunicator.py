
# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import
import logging
import socket
import time


from enocean.communicators.communicator import Communicator
from enocean.protocol.constants import PACKET
from enocean.protocol.packet import Packet


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
        self.sock.settimeout(3)
        pinged = time.time()
                
        try:
            self.sock.connect(( self.host, self.port))
        except Exception as e:
            self.logger.error('Exception occured while connecting: ' + str(e))
            self.stop()

        self.sock.settimeout(0.5)

        while not self._stop_flag.is_set():
            # If there's messages in transmit queue
            # send them
            while True:
                packet = self._get_from_send_queue()
                if not packet:
                    break
                try:
                    self.sock.send(bytearray(packet.build()))
                    pinged = time.time()
                except Exception as e:
                    self.logger.error('Exception occured while sending: ' + str(e))
                    self.stop()

            try:
                self._buffer.extend(bytearray(self.sock.recv(16)))
                self.parse()
            except socket.timeout:
                time.sleep(0)
            except ConnectionResetError as e:
                self.logger.error('Exception occured while recv: ' + str(e))
                self.stop()
            except Exception as e:
                self.logger.error('Exception occured while parsing: ' + str(e))
                
            time.sleep(0)
            if time.time() > pinged + 30:
                self.send(Packet(PACKET.COMMON_COMMAND, data=[0x08]))
                pinged = time.time()
          
        self.sock.close()
        self.logger.info('TCPClientCommunicator stopped')
