import os
import sys
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument('--input_dir', default='./22.real_XSS_URLs', help="input directory")
parser.add_argument('--out_pre_url_file', default='./22.pre_url.txt', help="output pre url filename")
parser.add_argument('--out_url_file', default='./22.url.txt', help="output url filename")

"""
USE this program ONLY on WEB sites constructed by JSP
INPUT FILES : in ZAP, Click Mouse Right button & Select 'Save Raw'
"""

def get_file_list(input_dir):
    fileList = []
    rootdir = input_dir

    for root, subFolders, files in os.walk(rootdir):
        for file in files:
            ext = os.path.splitext(file)[-1]
            if ext == ".raw":
                fileList.append(os.path.join(root, file))

    return sorted(fileList)

def touch_file(filename, header):
    now = datetime.now()
    now_str = now.strftime("%Y%m%d_%H%M%S")
    header_str = "# {} ({})\n".format(header, now_str)
    out_f = open(filename, 'w')
    out_f.write(header_str)
    out_f.close()

def add_text(filename, line):
    out_f = open(filename, 'a')
    out_f.write(line + "\n")
    out_f.close()

def get_xss_url(filename, out_pre_url_file, out_url_file):

    f = open(filename, 'r')

    text = f.read()

    f.close()

    line_list = text.split("\n")

    first_line = line_list[0]
    last_line = line_list[len(line_list)-1]

    first_line = first_line.strip()
    last_line = last_line.strip()

    url_list = first_line.split()
    if (url_list[0] == "GET"):
        my_url = "GET {}".format(url_list[1])
        print(my_url)

        add_text(out_pre_url_file, first_line)
        add_text(out_url_file, my_url)

        return

    if (url_list[0] == "POST"):
        # POST url?a=b  --data "c=d"
        if url_list[1].find('?') > 0 :
            my_url = "POST {}&{}".format(url_list[1], last_line)
        else:
            my_url = "POST {}?{}".format(url_list[1], last_line)
        print(my_url)

        add_text(out_pre_url_file, first_line)
        add_text(out_pre_url_file, last_line)
        add_text(out_url_file, my_url)

        return

if __name__ == '__main__':
    args = parser.parse_args()

    assert os.path.isdir(args.input_dir), "Couldn't find the given directory {}".format(args.input_dir)

    file_list = get_file_list(args.input_dir)

    print(file_list)

    touch_file(args.out_pre_url_file, "pre_url_file")
    touch_file(args.out_url_file, "url_file")

    for file in file_list:
        get_xss_url(file, args.out_pre_url_file, args.out_url_file)

    print("\n\npython ~/webhack_storage/PROJECT_K/ZAP_RESULT/XSS/23.REFINE_XSS_URL.py")
    print("  [--input_url_file 22.url.txt --output_url_file 23.refined_url.txt]\n\n")
