import os
import sys
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument('--input_dir', default='./22.example_SQL_URLs', help="input directory")
parser.add_argument('--out_pre_url_file', default='./22.pre_sqlmap_url.txt', help="output pre sql url filename")
parser.add_argument('--out_url_file', default='./22.sqlmap_url.txt', help="output sql url filename")

injection_code_list = []
injection_code_len = 0


def load_injection_code(inj_code_filename):
    global injection_code_len

    with open(inj_code_filename, 'r') as f:
        while 1:
            line = f.readline()
            if not line: break
            line = line.strip()

            injection_code_list.append(line)

    #print("len-->{}".format(len(injection_code_list)))
    injection_code_len = len(injection_code_list)

def get_injection_code_idx(my_url):
    for i in range(injection_code_len):
        if injection_code_list[i] in my_url:
            return i

    return -1

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
    out_f.write("#rm -rf ~/.sqlmap/output/YOUR_DOMAIN/\n")
    out_f.close()

def add_text(filename, line):
    out_f = open(filename, 'a')
    out_f.write(line + "\n")
    out_f.close()

def get_key(url_kv):
    url_key = url_kv.split("=")[0]
 
    return url_key


def get_refined_url_get(org_url):
    injection_code_idx = get_injection_code_idx(org_url)

    # not found
    if injection_code_idx < 0:
        return org_url, "NONE_1"

    new_url = org_url.replace(injection_code_list[injection_code_idx], "")
    
    idx = org_url.index('?')

    url_head = org_url[:idx]
    url_kv_str = org_url[idx+1:]

    url_kv_list = url_kv_str.split('&')

    new_key = "NONE_2"
    for url_kv in url_kv_list:
        if injection_code_list[injection_code_idx] in url_kv:
            new_key = get_key(url_kv)
            break

    return new_url, new_key

def get_refined_url_post(org_url, org_url2):
    injection_code_idx = get_injection_code_idx(org_url)
    injection_code_idx2 = get_injection_code_idx(org_url2)

    if injection_code_idx < 0 and injection_code_idx2 < 0:
        return org_url, org_url2, "NONE_3"

    if injection_code_idx >= 0:
        new_url = org_url.replace(injection_code_list[injection_code_idx], "")
        idx = org_url.index('?')
        url_head = org_url[:idx]
        url_kv_str = org_url[idx+1:]

        url_kv_list = url_kv_str.split('&')

        new_key = "NONE_4"
        for url_kv in url_kv_list:
            if injection_code_list[injection_code_idx] in url_kv:
                new_key = get_key(url_kv)
                break

        return new_url, org_url2, new_key

    if injection_code_idx2 >= 0:
        new_url2 = org_url2.replace(injection_code_list[injection_code_idx2], "")
        url_kv_list = org_url2.split('&')
      
        new_key = "NONE_5"
        for url_kv in url_kv_list:
            if injection_code_list[injection_code_idx2] in url_kv:
                new_key = get_key(url_kv)
                break

        return org_url, new_url2, new_key


def get_refined_url_rec(url_rec):
    url_rec_list = url_rec.split(" ")

    if url_rec_list[0] == "GET":
        refined_url, target_key = get_refined_url_get(url_rec_list[1])
        refined_url_rec = "{} {}".format(refined_url, target_key)

    if url_rec_list[0] == "POST":
        refined_url, refined_url2, target_key = get_refined_url_post(url_rec_list[1], url_rec_list[2])
        refined_url_rec = "{} {} {}".format(refined_url, refined_url2, target_key)
    
    return refined_url_rec

def make_sqlmap_command(url_rec):
    sqlmap_command = "#NONE"
    url_rec_list = url_rec.split(" ")
    if len(url_rec_list) == 2:
        sqlmap_command = "sqlmap -u \"{}\" -p {}".format(url_rec_list[0], url_rec_list[1])

    if len(url_rec_list) == 3:
        sqlmap_command = "sqlmap -u \"{}\" --data \"{}\" -p {}".format(url_rec_list[0], url_rec_list[1], url_rec_list[2])

    return sqlmap_command




def get_pre_sqlmap_url(filename, out_pre_url_file, out_url_file):

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
        url_rec = "{} {}".format(url_list[0], url_list[1])
        refined_url_rec = get_refined_url_rec(url_rec)
        #print("{}\n{}".format(url_rec, refined_url_rec))

        add_text(out_pre_url_file, url_rec)
        add_text(out_url_file, make_sqlmap_command(refined_url_rec))

        return

    if (url_list[0] == "POST"):
        # POST url?a=b  --data "c=d"
        url_rec = "{} {} {}".format(url_list[0], url_list[1], last_line)
        refined_url_rec = get_refined_url_rec(url_rec)
        #print("{}\n{}".format(url_rec, refined_url_rec))

        add_text(out_pre_url_file, url_rec)
        add_text(out_url_file, make_sqlmap_command(refined_url_rec))

        return


if __name__ == '__main__':
    args = parser.parse_args()

    assert os.path.isdir(args.input_dir), "Couldn't find the given directory {}".format(args.input_dir)

    file_list = get_file_list(args.input_dir)

    #print(file_list)

    touch_file(args.out_pre_url_file, "pre_url_file")
    touch_file(args.out_url_file, "url_file")

    load_injection_code("./sql_injection_type_stack.txt.uniq")

    #print(injection_code_len)
    #print(injection_code_list)

    for file in file_list:
        get_pre_sqlmap_url(file, args.out_pre_url_file, args.out_url_file)


    print("\n\nbash {}\n\n".format(args.out_url_file))
