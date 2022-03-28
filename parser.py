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

    def spdx_license_loader(self, path=SPDX_LICENSES):
        license_list = list()
        for license in os.listdir(path):
            print(license)

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

        license_grams = list()
        for i in spdx_license:
            template = i
            license_text = i['licenseText']
            license_header = i['standardLicenseHeader']
            if license_text != None:
                    template['licenseText'] = tokenizer.get_grams_from_license(license_text.split(' '))
            if license_header != None:
                 template['standardLicenseHeader']  = tokenizer.get_grams_from_license(license_header.split(' '))
            
            license_grams.append(template)
        
        #pd.DataFrame(license_grams).to_json('spdx_license_data_grams.json')
        with open('spdx_license_data_grams.json', 'w') as f:
            json.dump(license_grams, f)

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

if __name__ == '__main__':
    main()