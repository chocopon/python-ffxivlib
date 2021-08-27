# from bard import main
from jobhud import JobHudEntry
import pymem
from target import Target
from hotbar import HotbarList
from chat import ChatEntry
import win32gui


class FFXIV_LIB(object):
    '''
    '''
    battle_ptr = 0x1DDA5B0
    my_id_ptr  = 0x1DAA7A4
    def is_active(self):
        w = win32gui
        title = w.GetWindowText (w.GetForegroundWindow())
        return title == 'FINAL FANTASY XIV'    


    def __init__(self):
        self.ffxiv = pymem.Pymem('ffxiv_dx11.exe')
        self.target = Target(self.ffxiv)
        self.hotbar = HotbarList(self.ffxiv)
        self.chat = ChatEntry(self.ffxiv)
        self.jobhud = JobHudEntry(self.ffxiv)


    def get_new_chatlogs(self):
        return self.chat.get_new_chatlogs()


    def get_hotbars(self):
        return self.hotbar.get_hotbars()

    
    def get_current_target(self):
        return self.target.get_target_entity()


    def get_jobhud(self):
        return self.jobhud.get_jobhud()

    
    def is_battle(self):
        ptr = self.ffxiv.base_address + self.battle_ptr
        return self.ffxiv.read_bool(ptr)
    
    def get_myid(self):
        ptr = self.ffxiv.base_address + self.my_id_ptr
        return self.ffxiv.read_int(ptr)


if __name__ == "__main__":
    ffxiv = FFXIV_LIB()
    print(ffxiv.is_battle())
    print(ffxiv.get_myid())