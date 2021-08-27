import pymem
import struct

class JobHudEntry(object):
    '''
    '''
    PTR = [0x01DB3400, 0x18, 0x1938, 0x288, 0x20, 0x0]
    def __init__(self, ffxiv):
        self.ffxiv = ffxiv
        self.entry = self.__entry()
        # hents = []
        # for i in range(10):
        #     hents.append(self.entry + 0x400 * i)
        # self.hotbar_entries = hents


    def __entry(self):
        ptr = self.ffxiv.base_address
        for pt in self.PTR[:-1]:
            print(hex(ptr + pt))
            ptr = self.ffxiv.read_ulonglong(ptr + pt)
        ptr += self.PTR[-1]
        return ptr


    def get_jobhud(self):
        '''
        '''
        array = self.ffxiv.read_bytes(self.entry, 0x40)
        return JobHud(array)


class JobHud(object):
    '''
    '''
    def __init__(self, array):
        array    
        fields = {
            'hudtype'   :{'offset': 0x00,   'type': 'I',  'astype': 'int'},
            'remain'    :{'offset': 0x04,   'type': 'I',  'astype': 'int'}, 
            'start'     :{'offset': 0x08,   'type': 'I',  'astype': 'int'}, 
            'count'     :{'offset': 0x0C,   'type': 'I',  'astype': 'int'}, 
        }
        for k, v in fields.items():
            offset = v['offset']
            field = struct.unpack_from(v['type'], array, offset)
            field = field[0]
            setattr(self, k, field)


if __name__ == "__main__":
    ffxiv = pymem.Pymem('ffxiv_dx11.exe')
    jobhudentry = JobHudEntry(ffxiv)
    print(hex(jobhudentry.entry))
    print(jobhudentry.get_jobhud().remain)
    print(jobhudentry.get_jobhud().hudtype)
