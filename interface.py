import argparse
import json
from tkinter import E
from token_compare import TokenComapre 
from tqdm import tqdm
from parser import *
from tokenizer import *
from engine import *

SPDX_LICENSES = '/home/moonsun/spdx_project/spdx_license/'
SPDX_LICENSES_GRAMS = '/home/moonsun/spdx_project/spdx_license_data_grams.json'

# argv
arg_parser = argparse.ArgumentParser(description='Source code license detector.')
arg_parser.add_argument('--db', default=None, required=False, help='set spdx license directory')
arg_parser.add_argument('--find', type=str, default=None, required=False, help='set the directory to license check.')
args = arg_parser.parse_args()


# spdx 라이선스에서 ngram 데이터베이스 생성
if args.db != None:
    print('[+] Generate license database.')
    #try:
        # config 파일에 저장된 파일 경로 받도록 하자.
    parser = Parser()
    parser.spdx_license_database_generator()
    #except:
    #    exit('\n[!] check license database.')
    print('[+] Done.')


elif args.find != None:
    print('[+] Detecting source code licenses.')
    #try:
    parser = Parser()
    source_code_pathes = parser.source_code_path_loader(args.find)
    #except:
    #    exit('[!] check target path.')
    
    print('[*] Loading database ...')
    engine = Engine(SPDX_LICENSES_GRAMS, source_code_pathes)
    report_licenses, report_laod_error = engine.spdx_licese_finer()
    # Compare source code N-gram and spdx license database
    #compare = TokenComapre()

    with open('test_reulst.json', 'w') as f:
        json.dump(report_licenses, f)
    print('[+] Done.')
    #print(report_laod_error)

else:
    exit(arg_parser.print_help())