import os

import pyautogui

# 해상도를 구해서 Y값을 반환
def get_win_last_pos_y():
    return pyautogui.size()[1]


class Config():
    def __init__(self, config_filename):
        self.config_filename = config_filename
        self.total_url_count = 10
        self.win_url_count = 10
        self.win_s_pos_x = 0
        self.win_s_pos_y = 0
        self.win_out_file_pos_x = 0
        self.win_out_file_pos_y = 0
        self.prefix = 'xss'
        self.win_last_pos_y = 1080
        self.stop_count = 3
 
        self.save_dir = "./out_dir"

        self.step_Y = 21
        self.win_save_raw_pos_y_step = 100
       
        self.win_save_raw_pos_x_step = 100

        self.win_req_pos_y_step = 92
   
        self.win_req_pos_x_step = 360

        self.win_req_header_y_step = 142

        self.win_req_header_x_step = 458
 
        if os.path.exists(self.config_filename):
            self.make_config_dict_from_file()
            self.total_url_count = int(self.config_dict['total_url_count'])
            self.win_url_count = int(self.config_dict['win_url_count'])
            self.win_s_pos_x = int(self.config_dict['win_s_pos_x'])
            self.win_s_pos_y = int(self.config_dict['win_s_pos_y'])
            self.win_out_file_pos_x = int(self.config_dict['win_out_file_pos_x'])
            self.win_out_file_pos_y = int(self.config_dict['win_out_file_pos_y'])
            self.prefix = self.config_dict['prefix']
            self.win_last_pos_y = int(self.config_dict['win_last_pos_y'])
            self.stop_count = int(self.config_dict['stop_count'])

            self.save_dir = self.config_dict['save_dir']

            # check 'Y' position...
            self.step_Y = int(self.config_dict['step_Y'])
            self.win_save_raw_pos_y_step = int(self.config_dict['win_save_raw_pos_y_step'])
            self.win_save_raw_pos_x_step = int(self.config_dict['win_save_raw_pos_x_step'])
            self.win_req_pos_y_step = int(self.config_dict['win_req_pos_y_step'])
            self.win_req_pos_x_step = int(self.config_dict['win_req_pos_x_step'])
            self.win_req_header_y_step = int(self.config_dict['win_req_header_y_step'])
            self.win_req_header_x_step = int(self.config_dict['win_req_header_x_step'])

        self.win_save_raw_pos_y = self.win_last_pos_y - self.win_save_raw_pos_y_step

        self.win_req_pos_y = self.win_last_pos_y - self.win_req_pos_y_step

        self.win_req_header_y = self.win_last_pos_y - self.win_req_header_y_step

        # update win_last_pos_y
        self.win_last_pos_y = get_win_last_pos_y()
        self.config_dict['win_last_pos_y'] = str(self.win_last_pos_y)

    def reload(self):
        self.make_config_dict_from_file()

        self.total_url_count = int(self.config_dict['total_url_count'])
        self.win_url_count = int(self.config_dict['win_url_count'])
        self.win_s_pos_x = int(self.config_dict['win_s_pos_x'])
        self.win_s_pos_y = int(self.config_dict['win_s_pos_y'])
        self.win_out_file_pos_x = int(self.config_dict['win_out_file_pos_x'])
        self.win_out_file_pos_y = int(self.config_dict['win_out_file_pos_y'])
        self.prefix = self.config_dict['prefix']
        self.win_last_pos_y = int(self.config_dict['win_last_pos_y'])
        self.stop_count = int(self.config_dict['stop_count'])

        self.save_dir = self.config_dict['save_dir']

        # check 'Y' position...
        self.step_Y = int(self.config_dict['step_Y'])
        self.win_save_raw_pos_y_step = int(self.config_dict['win_save_raw_pos_y_step'])
        self.win_save_raw_pos_x_step = int(self.config_dict['win_save_raw_pos_x_step'])
        self.win_req_pos_y_step = int(self.config_dict['win_req_pos_y_step'])
        self.win_req_pos_x_step = int(self.config_dict['win_req_pos_x_step'])
        self.win_req_header_y_step = int(self.config_dict['win_req_header_y_step'])
        self.win_req_header_x_step = int(self.config_dict['win_req_header_x_step'])

        self.win_save_raw_pos_y = self.win_last_pos_y - self.win_save_raw_pos_y_step

        self.win_req_pos_y = self.win_last_pos_y - self.win_req_pos_y_step

        self.win_req_header_y = self.win_last_pos_y - self.win_req_header_y_step


    def make_config_dict_from_file(self):
        self.config_dict = {}

        f = open(self.config_filename, 'r')

        while 1:
            line = f.readline()
            if not line: break

            line = line.strip()

            # Skip blank line
            if (len(line) < 3): continue

            # Skip comment line
            if (line[0] == '#'): continue

            print ("({})".format(line))
            if line.find("=") < 0: continue
            key = line.split(" = ")[0].strip()
            val = line.split(" = ")[1].strip()

            self.config_dict[key] = val

        f.close()

    def make_config_dict_from_self(self):
        self.config_dict = {}
        self.config_dict['total_url_count'] = str(self.total_url_count)
        self.config_dict['win_url_count'] = str(self.win_url_count)
        self.config_dict['win_s_pos_x'] = str(self.win_s_pos_x)
        self.config_dict['win_s_pos_y'] = str(self.win_s_pos_y)
        self.config_dict['win_out_file_pos_x'] = str(self.win_out_file_pos_x)
        self.config_dict['win_out_file_pos_y'] = str(self.win_out_file_pos_y)
        self.config_dict['prefix'] = str(self.prefix)
        self.config_dict['win_last_pos_y'] = str(self.win_last_pos_y)
        self.config_dict['stop_count'] = str(self.stop_count)
        self.config_dict['save_dir'] = str(self.save_dir)
        self.config_dict['win_save_raw_pos_y_step'] = str(self.win_save_raw_pos_y_step)
        self.config_dict['win_req_pos_y_step'] = str(self.win_req_pos_y_step)
        self.config_dict['win_req_header_y_step'] = str(self.win_req_header_y_step)

    def update_config_dict(self, k, v):
        self.config_dict[k] = v

    def save_config_file(self):
        config_template_filename = "{}-TEMPLATE".format(self.config_filename)
        in_f = open(config_template_filename, 'r')
        text = in_f.read()
        in_f.close()

        for k, v in self.config_dict.items():
            text_key = "_{}_".format(k.upper())
            print("{}({}) -> {}".format(k, text_key, v))
            text = text.replace(text_key, v)

        out_f = open(self.config_filename, 'w')
        out_f.write(text)
        out_f.close()

    def print_config_dict(self):
        print("dump dict...")
        for k, v in self.config_dict.items():
            print("({}) -> ({})".format(k, v))

    def print_config_val(self):
        print("print_config_val()")
        print("self.total_url_count={}".format(self.total_url_count))
        print("self.win_url_count={}".format(self.win_url_count))
        print("self.win_s_pos_x={}".format(self.win_s_pos_x))
        print("self.win_s_pos_y={}".format(self.win_s_pos_y))
        print("self.win_out_file_pos_x={}".format(self.win_out_file_pos_x))
        print("self.win_out_file_pos_y={}".format(self.win_out_file_pos_y))
        print("self.prefix={}".format(self.prefix))
        print("self.win_last_pos_y={}".format(self.win_last_pos_y))
        print("self.stop_count={}".format(self.stop_count))

        print("self.step_Y={}".format(self.step_Y))

        print("self.win_save_raw_pos_x_step={}".format(self.win_save_raw_pos_x_step))
        print("self.win_save_raw_pos_y_step={}".format(self.win_save_raw_pos_y_step))
        print("self.win_save_raw_pos_y={}".format(self.win_save_raw_pos_y))


        print("self.win_req_pos_x_step={}".format(self.win_req_pos_x_step))
        print("self.win_req_pos_y_step={}".format(self.win_req_pos_y_step))
        print("self.win_req_pos_y={}".format(self.win_req_pos_y))

        print("self.win_req_header_x_step={}".format(self.win_req_header_x_step))
        print("self.win_req_header_y_step={}".format(self.win_req_header_y_step))
        print("self.win_req_header_y={}".format(self.win_req_header_y))


if __name__ == '__main__':
    cfg = Config('config.txt')
    cfg.print_config_dict()
    cfg.print_config_val()
    #cfg.update_config_dict("stop_count", "9")
    #cfg.save_config_file()

    #cfg.reload()
    #cfg.print_config_val()
    print("cfg.stop_count = {}".format(cfg.stop_count))



