import logging
import time
from ffxivlib import FFXIV_LIB
import keyboard
from datetime import datetime, timedelta

def get_action(action_id, hotbars):
    '''
    '''
    return get_action_pos(action_id, hotbars)[2]


def get_action_pos(action_id, hotbars):
    for b in range(10):
        hotbar = hotbars[b]
        for c in range(12):
            action = hotbar[c]
            if action.action_id == action_id:
                return b, c, action
    return None


def get_key_from_action_pos(pos):
    keys = ['1', '2', '3' ,'4' ,'5' , '6', '7', '8', '9', '0', '-', '^']
    if pos[0] == 0:
        return keys[pos[1]]
    if pos[0] == 1:
        return 'ctrl+'+ keys[pos[1]]
    return None


def do_action(action_id, hbars):
    ap = get_action_pos(action_id, hbars)
    if ap and ap[2].enable and ap[2].percent == 0 and ap[2].in_range:
        print('action:', action_id)
        # print(action_id, ap[2].enable, ap[2].percent, ap[2].in_range)
        key = get_key_from_action_pos(ap)
        keyboard.press_and_release(key)
        return True
    return False

# hoge = get_action_pos(100)
# print(hoge)
# import pdb; pdb.set_trace()

def main():
    while True:
        try:
            ffxiv = FFXIV_LIB()
            loop(ffxiv)
        except KeyboardInterrupt:
            return
        except Exception as e:
            time.sleep(10)      

def loop(ffxiv):
    print('loop start')
    rain = False
    start = True
    # log 捨て
    ffxiv.get_new_chatlogs()
    last_log_time = datetime.now()

    while True:
        time.sleep(0.2)
        for log in ffxiv.get_new_chatlogs():
            last_log_time = datetime.now()
            if log.body.startswith('/reset'):
                print('reset')
                return
            if log.body.startswith('/start'):
                print('start')
                start = True
            if log.body.startswith('/stop'):
                print('stop')
                start = False
            if log.body.startswith('/rain'):
                rain = True
            if log.body.startswith('/blood'):
                rain = False
        if last_log_time < datetime.now() - timedelta(seconds=60):
            # チャットログが更新されてない場合はリスタート
            print('no logs long time. restart')
            return

        if start and ffxiv.is_active() and ffxiv.is_battle():
            ct = ffxiv.get_current_target()
            hbars = ffxiv.get_hotbars()
            jobhud = ffxiv.get_jobhud()
            myid = ffxiv.get_myid()
            if ct is not None:
                ct_mybuffs =  [x for x in ct.buffs if x.buff_provider == myid]
                blood = get_action(110, hbars)
                menu = get_action(3559, hbars)
                bara = get_action(114, hbars)
                pion = get_action(116, hbars)
                # 詩パート
                # 旅神のメヌエット
                if do_action(3559, hbars):
                    continue
                # 賢人のバラード 114
                if menu.cost < 50:
                    if do_action(114, hbars):
                        continue
                # 軍神のパイオン 116、バラード発動後30秒後
                if menu.cost < 20 and bara.cost < 50:
                    if do_action(116, hbars):
                        continue

                # アビリティパート
                # 猛者の撃 101
                if do_action(101, hbars):
                    continue

                # バトルボイス 118
                if do_action(118, hbars):
                    continue

                # 乱れうち 107
                if do_action(107, hbars):
                    continue

                # ピッチパーフェクト
                if jobhud.hudtype==3 and (  jobhud.count == 3 or 
                                            jobhud.remain <= 1000):
                    if do_action(7404, hbars):
                        continue

                # エンピリアルアロー
                if do_action(3558, hbars):
                    continue

                # サイドワインダー
                if any([x.id == 1310844 or x.id == 2622640 for x in ct_mybuffs]) and any([x.id == 1310849 or x.id == 2622641 for x in ct_mybuffs]):
                    if do_action(3562, hbars):
                        continue
                
                # アイアンジョー
                dot_debuffs = [x for x in ct_mybuffs if x.id in [1310844,2622640,1310849,2622641]]
                if len(dot_debuffs) > 0:
                    dot_debuffs.sort(key=lambda x: x.time_left)
                    if dot_debuffs[0].time_left < 5:
                         if do_action(3560, hbars):
                            continue

                # Weapon Skill
                # ストレートショット 98
                if do_action(98, hbars):
                    continue
                # ベノムバイト　100 debuff:1310844
                # コースティックバイト  2622640
                if not any([x.id == 1310844 or x.id == 2622640 for x in ct_mybuffs]):
                    if do_action(100, hbars):
                        continue

                # ウインドバイト　113 debuff:1310849
                # ストームバイト  113 2622641
                if not any([x.id == 1310849 or x.id == 2622641 for x in ct_mybuffs]):
                    if do_action(113, hbars):
                        continue

                if rain:
                    # レインオオブデス 117
                    if do_action(117, hbars):
                        continue
                    # クイックノック 106
                    if do_action(106, hbars):
                        continue
                else:
                    # ブラッドレッター 110
                    if do_action(110, hbars):
                        continue
                    # ヘヴィショット 97
                    if do_action(97, hbars):
                        continue
                
                
if __name__ == "__main__":
    main()
