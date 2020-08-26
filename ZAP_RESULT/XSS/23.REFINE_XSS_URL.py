import os
import sys
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument('--input_url_file', default='./22.url.txt', help="input url filename")
parser.add_argument('--output_url_file', default='./23.refined_url.txt', help="output url filename")
parser.add_argument('--modify', '-m', action='store_true', help="modify alert")

url_path_key_dict = {}

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

def get_url_list(in_file):
    url_list = []
    in_f = open(in_file, 'r')
    while 1:
        line = in_f.readline()
        if not line: break
        line = line.strip()
        if line[0] == '#': continue
        url_list.append(line)
    
    in_f.close()
    
    return url_list

def get_url_path_and_query_key(url):
    idx = url.index("?")
    url_path = url[:idx]
    url_queries = url[idx+1:]
    
    query_key = None
    url_query_list = url_queries.split('&')
    for url_query in url_query_list:
        #print(":: {}".format(url_query))
        if (url_query.find("alert") > 0):
            query_key = url_query.split('=')[0]
            break
    
    return url_path, query_key

def add_url_path_key_to_dict(url_path, query_key, url):
    key = "{}\t{}".format(url_path, query_key)
    val = url
    if key in url_path_key_dict:
        url_list = url_path_key_dict[key]
        url_list.append(val)
    else:
        url_list = [val]
        url_path_key_dict[key] = url_list

def dump_dict(my_dict):
    for k, v_list in my_dict.items():
        print("{}".format(k))
        for v in v_list:
            print("\t{}".format(v))

def make_meta_dict(sorted_keys):
    meta_dict = {}
    for kv in sorted_keys:
        k = kv.split('\t')[0]
        v = kv.split('\t')[1]
        if k in meta_dict:
            v_list = meta_dict[k]
            v_list.append(v)
        else:
            meta_dict[k] = [v]
        
    return meta_dict

if __name__ == '__main__':
    args = parser.parse_args()

    assert os.path.isfile(args.input_url_file), "Couldn't find the given file {}".format(args.input_url_file)

    touch_file(args.output_url_file, "refined_url_file")

    print("\n{} --> {}".format(args.input_url_file, args.output_url_file))
    print("\nmodify option = {}\n\n".format(args.modify))
   
    url_list = get_url_list(args.input_url_file)
    for url in url_list:
        url_path, query_key = get_url_path_and_query_key(url)
        add_url_path_key_to_dict(url_path, query_key, url)

    #dump_dict(url_path_key_dict)

    #sorted_url_path_key_dict = get_sorted_dict(url_path_key_dict)

    sorted_keys = sorted(url_path_key_dict.keys())

    meta_dict = make_meta_dict(sorted_keys)
    
    seq = 1
    meta_sorted_keys = sorted(meta_dict.keys())
    for k in meta_sorted_keys:
        txt = "\n{:03d}) {}".format(seq, k)
        add_text(args.output_url_file, txt)
        v_list = meta_dict[k]
        for v in v_list:
            #print ("{}\t{}".format(k, v))
            txt = "\t({})".format(v)
            add_text(args.output_url_file, txt)
            my_key = "{}\t{}".format(k, v)
            my_v_list = url_path_key_dict[my_key]
            for my_v in my_v_list:
                txt = "\t{}".format(my_v)
                # alert(1) -> alert(9876)
                if args.modify == True:
                    txt = txt.replace("%281","%289876")
                add_text(args.output_url_file, txt)

        seq += 1

    """
    for k in sorted_keys:
        add_text(args.output_url_file, k)
        v_list = url_path_key_dict[k]
        for v in v_list:
            txt = "\t{}".format(v)
            add_text(args.output_url_file, txt)
    """
