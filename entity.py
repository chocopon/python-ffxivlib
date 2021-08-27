import struct
from buff import Buff

class Entity(object):
    '''キャラクター、オブジェクト情報
    '''
    def __init__(self, array):
        fields = {
            'name'      :{'offset': 0x30,   'type': '32s',  'astype': 'string'},
            'char_id'   :{'offset': 0x74,   'type': 'I',   'astype': 'int'}, # CharID
            'x'         :{'offset': 0xA0,   'type': 'f',    'astype': 'float'}, # E-W
            'z'         :{'offset': 0xA4,   'type': 'f',    'astype': 'float'}, # L-H
            'y'         :{'offset': 0xA8,   'type': 'f',    'astype': 'float'}, # N-S
            'heading'   :{'offset': 0xB0,   'type': 'f',    'astype': 'float'}, # Direction S=0 N= +-3.14
            'is_red'    :{'offset': 0x0F6C, 'type': '?',    'astype': 'bool'}, # 24*12
            'buffs'     :{'offset': 0x19F8, 'type': '288s', 'astype': 'buff[]'}, # 24*12
        }
        for k, v in fields.items():
            offset = v['offset']
            field = struct.unpack_from(v['type'], array, offset)
            if      v['astype'] == 'string':
                field = field[0].decode(encoding="utf-8", errors="ignore").split('\0')[0]
            elif    v['astype'] == 'buff[]':
                field = Buff.parse(bytearray(field[0]))
            else:
                field = field[0]
            setattr(self, k, field)

