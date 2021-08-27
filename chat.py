import pymem

class ChatLog(object):
    
    def __init__(self, headarray, namearray, bodyarray):
        self.headarray = headarray
        self.namearray = namearray
        self.bodyarray = bodyarray

        self.body = ChatLog.remove_transtags(bodyarray).decode('utf-8', errors='ignore')
        self.name = ChatLog.remove_transtags(namearray).decode('utf-8', errors='ignore')

    @staticmethod
    def remove_transtags(array):
        '''翻訳タグを削除する
        '''
        flg = False
        data = []
        for c in array:
            if flg and c == 0x03:
                flg = False
            elif c == 0x02:
                flg = True
            if flg:
                continue
            data.append(c)
        return bytearray(data)


class ChatEntry(object):
    ptrs = [0x01D8DE88, 0x85B0]

    def __init__(self, ffxiv):
        '''
        '''
        self.ffxiv = ffxiv
        self.update_ptr()


    def __get_data_array(self, array):
        '''
        '''
        chat_array = []
        cn_flg = False
        head = None
        name = None
        body = None

        data = []
        i = 0
        while i < len(array):
            if array[i] == 0x1F and cn_flg:
                name = bytearray(data)
                cn_flg = False
                data = []

            elif array[i] == 0x1F:
                if i > 10:
                    body = bytearray(data[:-8])
                    chat_array.append(ChatLog(head, name, body))
                head = bytearray(data[-8:])
                cn_flg = True
                data = []

            else:
                data.append(array[i])
            i += 1

        body = bytearray(data)
        chat_array.append(ChatLog(head, name, body))
        return chat_array


    def update_ptr(self):
        '''
        '''
        ad = self.ffxiv.base_address
        for ptr in self.ptrs:
            ad = self.ffxiv.read_ulonglong(ad + ptr)
        self.count_ad = ad + 0x14
        self.array_start_pt = ad + 0x60
        self.array_end_pt = ad + 0x68
        array_start = self.ffxiv.read_longlong(self.array_start_pt)
        self.last = array_start


    def get_new_chatlogs(self):
        '''
        '''
        array_end   = self.ffxiv.read_longlong(self.array_end_pt)
        if array_end < self.last:
            self.update_ptr()
            return self.get_new_chatlogs()

        if array_end > self.last:
            array = self.ffxiv.read_bytes(self.last, (array_end - self.last))
            self.last = array_end
            return self.__get_data_array(array)
        return []


if __name__ == "__main__":
    ffxiv = pymem.Pymem('ffxiv_dx11.exe')
    chatentry = ChatEntry(ffxiv)
    logs = chatentry.get_new_chatlogs()
    for log in logs:
        print(log.name, log.body)

    while True:
        for log in chatentry.get_new_chatlogs():
            print(log.body)