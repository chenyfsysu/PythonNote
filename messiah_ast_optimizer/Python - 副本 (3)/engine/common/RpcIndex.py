# -*- coding:utf-8 -*-

from hashlib import md5
from mobilelog.LogManager import LogManager
_logger = LogManager.get_logger('RpcIndexer')
VERIFY_TAG = '_v_e_r_i_f_y_'
DEFAULT_RECV_RPC_SALT = '0'
DEFAULT_SEND_RPC_SALT = '0'
try:
    from _PRESET_RPC_INDEXES import RPC2INDEX, INDEX2RPC, RECV_RPC_SALT, SEND_RPC_SALT, SEND_CACHE
    _logger.info('Using Preset RPC Indexes.')
    PRESET_RPC_INDEXES = True
except:
    _logger.info('No Preset RPC Indexes Found.')
    PRESET_RPC_INDEXES = False
    RPC2INDEX = {VERIFY_TAG: 0}
    INDEX2RPC = {}
    RECV_RPC_SALT = DEFAULT_RECV_RPC_SALT
    SEND_RPC_SALT = DEFAULT_SEND_RPC_SALT
    SEND_CACHE = {}

def register_rpc(rpcname):
    if (rpcname in RPC2INDEX):
        return
    index = recv_rpc_index(rpcname)
    if (index in INDEX2RPC):
        raise RuntimeError(('RPC INDEX Of [%s] AND [%s] ARE CONFLICTED WITH SALT %s!' % (rpcname, INDEX2RPC[index], RECV_RPC_SALT)))
    INDEX2RPC[index] = rpcname
    RPC2INDEX[rpcname] = index

def calculate_rpc_index(name, salt):
    m = md5()
    m.update((name + salt))
    b = m.digest()
    return (((((ord(b[(-4)]) & 127) << 24) + (ord(b[(-3)]) << 16)) + (ord(b[(-2)]) << 8)) + ord(b[(-1)]))

def recv_rpc_index(name):
    return calculate_rpc_index(name, RECV_RPC_SALT)

def send_rpc_index(name):
    index = SEND_CACHE.get(name, None)
    if (index is None):
        index = SEND_CACHE[name] = calculate_rpc_index(name, SEND_RPC_SALT)
    return index

def dump_preset_rpc_indexes_py(directory):
    import os
    filename = os.path.join(directory, '_PRESET_RPC_INDEXES.py')
    with open(filename, 'w') as f:
        f.write('# -*- coding: utf-8 -*-\n\n\n')
        f.write(('RPC2INDEX = %r\n' % RPC2INDEX))
        f.write(('INDEX2RPC = %r\n' % INDEX2RPC))
        f.write(('RECV_RPC_SALT = %r\n' % RECV_RPC_SALT))
        f.write(('SEND_RPC_SALT = %r\n' % SEND_RPC_SALT))
        f.write(('SEND_CACHE = %r\n' % SEND_CACHE))
    _logger.info('PRESET RPC Indexes Python File Dumped.')
