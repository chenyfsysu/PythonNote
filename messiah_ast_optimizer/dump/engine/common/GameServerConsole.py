# -*- coding:utf-8 -*-

'\n\xe6\xb8\xb8\xe6\x88\x8f\xe4\xb8\xad\xe4\xbd\xbf\xe7\x94\xa8\xe7\x9a\x84Telnet\xe7\xbb\x88\xe7\xab\xaf\xe3\x80\x82\n'
from common.mobilecommon import asiocore
from mobilelog.LogManager import LogManager

class GameServerConsole(asiocore.telnet_server, ):
    logger = LogManager.get_logger('Telnet')

    def __init__(self, ip='127.0.0.1', port=9113):
        super(GameServerConsole, self).__init__()
        while 1:
            try:
                if self.bind(ip, port):
                    break
            except Exception as e:
                self.logger.error('Failed To Bind Port %s:%d For %s', ip, port, e)
            port += 1
            if (port > 65535):
                raise IOError('Telnet Server Failed To Find A Usable Port To Bind!')
        self.logger.info('Telnet Server Binded on Port %s:%d', ip, port)
        self.ip = ip
        self.port = port

    def start(self):
        self.listen(5)

    @property
    def handler(self):
        import __main__
        return getattr(__main__, '_telnet_handler', None)

    @handler.setter
    def handler(self, handler):
        import __main__
        __main__._telnet_handler = handler
