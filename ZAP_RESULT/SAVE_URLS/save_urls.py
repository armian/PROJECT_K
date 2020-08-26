import argparse
import pyautogui
import time

from config import Config

parser = argparse.ArgumentParser()

parser.add_argument('--all', '-a', action='store_true', help="all flag")
parser.add_argument('--force', '-f', action='store_true', help="force flag")
parser.add_argument('--verbose', '-v', action='store_true', help="verbose flag")

def get_position():
    x, y = pyautogui.position()
    return x, y

class saveURL():
    def __init__(self, config_filename, verbose_flag, force_flag, all_flag):
        self.config_filename = config_filename

        self.cfg = Config(self.config_filename)

        self.verbose_flag = verbose_flag
        self.force_flag = force_flag
        self.all_flag = all_flag

    #def save_current_url(self, url_no, curpos_X, curpos_Y):
    def save_current_url(self, url_no):
        # url_no -> (0..N-1)
        #print("save_current_url...")
        curpos_X = self.cfg.win_s_pos_x
        if url_no < self.cfg.win_url_count:
            curpos_Y = self.cfg.win_s_pos_y + self.cfg.step_Y * url_no
        else:
            curpos_Y = self.cfg.win_s_pos_y + self.cfg.step_Y * (self.cfg.win_url_count - 1)
            pyautogui.moveTo(curpos_X, curpos_Y)
            time.sleep(0.1) 
            pyautogui.click()
            time.sleep(0.1)
            pyautogui.press('down')

        out_filename = "{}/{}_{:03d}".format(self.cfg.save_dir, self.cfg.prefix, url_no+1)

        print("({:03d}/{:03d}) -> {}".format(url_no+1, self.cfg.total_url_count, out_filename))

        time.sleep(0.3)
        if self.verbose_flag:
            print("\t- curpos : {},{}".format(curpos_X, curpos_Y))
        pyautogui.moveTo(curpos_X, curpos_Y)
        time.sleep(0.3)
        pyautogui.click()
        time.sleep(0.3)

        # 우클릭 (for 'save raw')
        pyautogui.click(button='right')
        time.sleep(0.2)

        # 'Save Raw'
        raw_pos_X = curpos_X + self.cfg.win_save_raw_pos_x_step
        raw_pos_Y = self.cfg.win_save_raw_pos_y
        if self.verbose_flag:
            print("\t- rawpos : {},{}".format(raw_pos_X, raw_pos_Y))
        pyautogui.moveTo(raw_pos_X, raw_pos_Y)
        time.sleep(0.1)

        # 'Request'
        req_pos_X = curpos_X + self.cfg.win_req_pos_x_step
        req_pos_Y = self.cfg.win_req_pos_y
        if self.verbose_flag:
            print("\t- req_pos : {},{}".format(req_pos_X, req_pos_Y))
        pyautogui.moveTo(req_pos_X, req_pos_Y)
        time.sleep(0.1)

        # 'Header' or 'all'
        # 무조건 'Header'로 이동한 다음, 'down' key를 두번 누른다.
        # POST의 경우 'all'이 존재하므로 아래로 이동되고,
        # GET의 경우 'all'이 존재하지 않으므로 그 자리에 멈추어 있게 된다.
        req_ha_pos_X = curpos_X + self.cfg.win_req_header_x_step
        req_ha_pos_Y = self.cfg.win_req_header_y

        if self.verbose_flag:
            print("\t- req_ha_pos : {},{}".format(req_ha_pos_X, req_ha_pos_Y))
        pyautogui.moveTo(req_ha_pos_X, req_ha_pos_Y)
        time.sleep(0.1)
        pyautogui.press('down')
        time.sleep(0.1)
        pyautogui.press('down')
        time.sleep(0.1)
    
        # pop up 'save menu'
        pyautogui.typewrite(['enter'])
        #pyautogui.click()
        time.sleep(0.1)

        # move to input window and type 'output filename'
        pyautogui.moveTo(self.cfg.win_out_file_pos_x, self.cfg.win_out_file_pos_y)
        pyautogui.click()
        time.sleep(0.1)

        #pyautogui.typewrite(out_filename)
        pyautogui.write(out_filename, interval=0.01)
        time.sleep(0.1)

        if self.force_flag == True:
            #pyautogui.moveTo(self.cfg.win_save_button_pos_x, self.cfg.win_save_button_pos_y)
            pyautogui.typewrite(['enter'])
            #pyautogui.click()
            time.sleep(0.1)
        else:
            # 메뉴 탈출 (나중에 수정필요)
            pyautogui.press('esc')
            time.sleep(0.1)
            pyautogui.press('esc')

if __name__ == '__main__':
    org_x, org_y = get_position()

    args = parser.parse_args()

    su = saveURL(args.verbose, args.force, args.all)

    su.save_urls()

    if args.force:
        print ("\n\npython ~/webhack_storage/COMMAND_TEMPLATE/22.MAKE_XSS_URL_FROM_DIR.py --input_dir [your_input_directory]\n\n")

    # 시작위치(터미널로)로
    pyautogui.moveTo(org_x, org_y)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.typewrite(['enter'])
    time.sleep(1)

    if args.force:
        pyautogui.typewrite("python ~/webhack_storage/COMMAND_TEMPLATE/22.MAKE_XSS_URL_FROM_DIR.py --input_dir ")
        time.sleep(0.1)
