import pymem
from entity import Entity

class Target(object):
    '''ターゲットへのポインタを取得
    '''
    PTS = [0x01DB8140]
    PTS = [0x01DAF140] # 09000
    def __init__(self, ffxiv):
        self.ffxiv = ffxiv
        self.entry = self.ffxiv.base_address + self.PTS[0]
        self.target_pt = self.entry + 0x0
        self.focus_target_pt = self.entry + 0x78
        self.last_target_pt = self.entry + 0x80


    def get_target_entity(self):
        '''
        '''
        address = self.ffxiv.read_ulonglong(self.target_pt)
        if address == 0:
            return None
        data = self.ffxiv.read_bytes(address, 0x2000)
        return Entity(data)


    def show(self):
        print('entry', hex(self.entry))
        print('target_pt', hex(self.target_pt))
        print('focus_target_pt', hex(self.focus_target_pt))
        print('last_target_pt', hex(self.last_target_pt))


if __name__ == "__main__":
    ffxiv = pymem.Pymem('ffxiv_dx11.exe')
    target = Target(ffxiv)
    print(hex(target.target_pt))
    print(hex(target.ffxiv.read_ulonglong(target.target_pt)))
    t = target.get_target_entity()
    if t is not None:
        print(t.name, t.is_red, hex(t.char_id))
        for buff in t.buffs:
            if buff.id != 0:
                print(buff.id, buff.time_left, buff.buff_provider)