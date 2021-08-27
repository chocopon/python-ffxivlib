import struct

class Buff(object):
    '''バフ
    '''
    def __init__(self, bytearray):
        data = struct.unpack_from('IfI', bytearray,0)
        self.id = data[0]
        self.time_left = data[1]
        self.buff_provider = data[2]


    @staticmethod
    def parse(bytearray):
        '''バイト列からバフを取得する。
        '''
        buffs = []
        for i in range(0, len(bytearray), 12):
            bdata = bytearray[i:i+12]
            buffs.append(Buff(bdata))
        return buffs
