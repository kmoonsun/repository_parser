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
    file_path_list = parser.source_code_path_loader(args.find)
    #except:
    #    exit('[!] check target path.')
    
    print('[*] Loading database ...')
    engine = Engine(SPDX_LICENSES_GRAMS)
    spdx_license_database = list(json.loads(open(SPDX_LICENSES_GRAMS,'r').read()))
    spdx_license_id_database = [list(i.keys())[0] for i in spdx_license_database]
    # Generate spdx_id hashtable
    tb_spdx_id = dict()
    for i in spdx_license_id_database:
        tb_spdx_id[i] = 0
    print('[*] Database load complete.')

    report_spdx_license = list()
    report_load_error = list()
    report_copyright = list()
   
    for source_code_path in tqdm(file_path_list, desc='progress', ncols=100, leave=True):
        try:
            with open(source_code_path, 'r') as f:
                source = f.read()
        except:
            report_load_error.append(source_code_path)
            continue
        # [개발예정] 감지된 확장자에 따라 다른 parser 호출 예정

        # Generate N-gram from source code
        comments = parser.c_comment_parser(source)
        tokenizer = Tokenizer()
        # comments : original comment list
        grams, words, comments = tokenizer.get_grams_from_source(comments)
      
        print(comments)
        # License detection based on SDPX_identifier.
        rst_template = dict() # 7:8
        for index, word in enumerate(words):
            if tb_spdx_id.get(word) != None:
                rst_template['name'] = source_code_path
                rst_template['license'] = word
                rst_template['index'] = index
                report_spdx_license.append(rst_template)
                break
            
        # Compare source code N-gram and spdx license database
        compare = TokenComapre()

        '''
        "licenseId": "TU-Berlin-1.0",
        "name": "Technische Universitaet Berlin License 1.0",
        "licenseText": [
        '''

        '''
        for license in spdx_license_database:
            scores = list()
            key = list(license.keys())
            # spdx-license 검증
            # a = list(filter(lambda x: key[0] in x, grams))
            
            # key[0] : spdx_license_id

            # text 검증
            # standard 검증
        '''

    print('[+] Done.')
    print(report_spdx_license)
    print('--------')
    print(report_load_error)

else:
    exit(arg_parser.print_help())