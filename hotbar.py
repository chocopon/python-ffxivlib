import pymem
from action import Action

class HotbarList(object):
    '''
    '''
    PTR = [0x1DB3400, 0x38, 0x18, 0x30, 0x20, 0x40]
    def __init__(self, ffxiv):
        self.ffxiv = ffxiv
        self.entry = self.__entry()
        hents = []
        for i in range(10):
            hents.append(self.entry + 0x400 * i)
        self.hotbar_entries = hents


    def __entry(self):
        ptr = self.ffxiv.base_address
        for pt in self.PTR[:-1]:
            # print(hex(ptr + pt))
            ptr = self.ffxiv.read_ulonglong(ptr + pt)
        ptr += self.PTR[-1]
        return ptr


    def get_hotbars(self):
        '''
        '''
        hotbars = []
        for ent in self.hotbar_entries:
            data = self.ffxiv.read_bytes(ent, 0x400)
            actions = []
            for i in range(12):
                action = Action(data[i * 0x40: i * 0x40 + 0x40])
                actions.append(action)
            hotbars.append(actions)
        return hotbars


if __name__ == "__main__":
    
    # import pdb; pdb.set_trace()
    ffxiv = pymem.Pymem('ffxiv_dx11.exe')
    hlist = HotbarList(ffxiv)
    hbars = hlist.get_hotbars()
    print(hex(hlist.entry))
    for hb in hbars:
        for ac in hb:
            print(ac.action_id)
    # print(hex(hlist.entry))
    # PTR = [0x02E3FB4A28, 0x790]

    # ptr = ffxiv.base_address
    # for pt in PTR[:-1]:
    #     print(hex(ptr))
    #     ptr = ffxiv.read_ulonglong(ptr + pt)
    #     print(hex(ptr))
    #     print()
    # ptr += PTR[-1]
    # print(hex(ptr))