import struct

class Action(object):
    def __init__(self, array):
        fields = {
            'action_type'   :{'offset': 0x00,   'type': 'I',    'astype': 'uint'}, # 0:ability 1: 2:cast
            'action_id'     :{'offset': 0x08,   'type': 'I',    'astype': 'uint'}, # 
            'enable'        :{'offset': 0x10,   'type': 'I',    'astype': 'bool'}, # enable:1, unable:0
            'percent'       :{'offset': 0x1C,   'type': 'I',    'astype': 'uint'}, # 100で0になる
            'cost'          :{'offset': 0x24,   'type': 'I',    'astype': 'uint'}, # リキャストの残り秒もここ
            'chain'         :{'offset': 0x34,   'type': 'I',    'astype': 'uint'}, # コンボのチェインがONのとき１
            'in_range'      :{'offset': 0x38,   'type': 'I',    'astype': 'bool'}, # 射程距離内か
        }
        for k, v in fields.items():
            offset = v['offset']
            field = struct.unpack_from(v['type'], array, offset)[0]
            if v['astype'] == 'bool':
                field = bool(field)
            setattr(self, k, field)