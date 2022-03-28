import argparse
import os 
from tqdm import tqdm
from parser import *
from tokenizer import *

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
    try:
        # config 파일에 저장된 파일 경로 받도록 하자.
        parser = Parser()
        parser.spdx_license_database_generator()
    except:
        exit('[!] check license database.')
    print('[+] Done.')

elif args.find != None:
    print('[+] Detecting source code licenses.')
    #try:
    parser = Parser()
    file_path_list = parser.source_code_path_loader(args.find)
    #except:
    #    exit('[!] check target path.')
    
    for source_code_path in tqdm(file_path_list, desc='progress', ncols=100):
        with open(source_code_path, 'r') as f:
            source = f.read()
        # [개발예정] 감지된 확장자에 따라 다른 parser 호출 예정
        comments = parser.c_comment_parser(source)

    print('[+] Done.')

else:
    exit(arg_parser.print_help())