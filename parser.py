from operator import index
import os
import sys
import json
import re
import itertools
import pandas as pd
from tokenizer import *

sys.path.append('/home/moonsun/spdx_project')
KEYWORD_SET = './keywords.json'
SPDX_LICENSES = '/home/moonsun/spdx_project/spdx_license/'
SPDX_LICENSES_GRAMS = '/home/moonsun/spdx_project/spdx_license_data_grams.json'

class Parser:
    def __init__(self):
        self.keyworkd_set = json.loads(open(KEYWORD_SET,'r').read())

    def c_comment_parser(self, source):
        # parse comment
        comment = re.findall(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', source, re.MULTILINE | re.DOTALL)
        # parse text, filtering empty elems 
        text = list(filter(None, [re.sub(r'\"(.*?)\"|\'(.*?)\'|[/*]|[\t\n]|  ', '', i).strip() for i in comment]))
        return text

    def source_code_path_loader(self, root_path=None):
       
        if root_path == None:
            exit('[!] file not found.')
        print(root_path)
        file_pathes = list()
        for root, dirs, files in os.walk(root_path):
            for file in files:
                ext = os.path.splitext(file)[-1].split('.')[-1]
                # 추후 exe 감지에 사용
                item = {'path' : root + '/' + file,
                        'ext' : ext
                }
                file_pathes.append(root+'/'+file)    

        return file_pathes

    def spdx_license_loader(self, path=SPDX_LICENSES):
        license_list = list()
        for license in os.listdir(path):
            read = json.load(open(path+license, 'r'))

            template = dict()
            tags = ['licenseId', 'name', 'licenseText', 'standardLicenseHeader']
            for tag in tags:
                try:
                    # remove whitespace and \n (2 more)
                    template[tag] = re.sub(r'\s\s+', ' ', read[tag]).replace('\n','')
                except:
                    template[tag] = None
            license_list.append(template)
        
        return license_list

    def spdx_license_database_generator(self, license_file_path=SPDX_LICENSES):
        tokenizer = Tokenizer()
        spdx_license = self.spdx_license_loader(license_file_path)
        length = len(spdx_license)

        license_grams = list()
        for index, i in enumerate(spdx_license):
            print(f'\r\t=> {index}/{length}', end='', flush=True)
            template = i
            license_text = i['licenseText']
            license_header = i['standardLicenseHeader']
            if license_text != None:
                    template['licenseText'] = tokenizer.get_grams_from_license(license_text.split(' '))
            if license_header != None:
                 template['standardLicenseHeader']  = tokenizer.get_grams_from_license(license_header.split(' '))
            
            license_grams.append(template)

        file_name = 'spdx_license_data_grams.json'
        print('\n[+] Save as "{f}"...'.format(f=file_name))
        with open(file_name, 'w') as f:
            json.dump(license_grams, f)

        return file_name


def main():
    root_directory = sys.argv[1]
    file_list = list()
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            ext = os.path.splitext(file)[-1].split('.')[-1]
            
            item = {'path' : root + '/' + file,
                    'ext' : ext
            }
            file_list.append(root+'/'+file)    

    with open(file_list[1], 'r') as fp:
        source = fp.read()

    parser = Parser()
    blocks = parser.c_comment_parser(source)
    #parser.spdx_license_database_generator()
    tokenizer = Tokenizer()
    grams = tokenizer.get_grams_from_source(blocks)

    token_compare = TokenComapre()
    lcs_score = token_compare.lcs_similarity(grams, token_compare.spdx_license_gram)
    print(lcs_score)



if __name__ == '__main__':
    main()