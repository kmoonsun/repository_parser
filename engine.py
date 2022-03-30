import json
from parser import *
from sre_parse import Tokenizer
from tokenizer import *

class Engine:
    report_spdx_licenses = list()  # 식별된 sdpx 라이선스
    report_load_errors = list()    # 읽을 수 없는 파일 (소스코드 아님)
    report_copyrights = list()     # 저작권 표기 정보

    # interface에 구현한 탐색 알고리즘 옮겨 담기 해야함.
    def __init__(self, license_db_path, source_code_pathes):
        self.spdx_license_kb = self.load_license_database_to_list(license_db_path)
        self.spdx_license_id_database = self.load_license_id_to_list()
        self.source_code_pathes = source_code_pathes

        # Init spdx_id hashtable
        self.tb_spdx_id = dict()
        for i in self.spdx_license_id_database:
            self.tb_spdx_id[i] = 0
    

    def load_license_database_to_list(self, path):
        return list(json.loads(open(path,'r').read()))
    

    def load_license_id_to_list(self):
        return [list(i.keys())[0] for i in self.spdx_license_kb]


    def spdx_licese_finer(self):
        parser = Parser()
        tokenizer = Tokenizer()
        # Hard copy for multithread
        tb_spdx_id = self.tb_spdx_id
        source_code_pathes = self.source_code_pathes

        # Process
        # for source_code_path in tqdm(source_code_pathes, desc='progress', ncols=100, leave=True):
        for source_code_path in source_code_pathes:
            try:
                with open(source_code_path, 'r') as f:
                    source = f.read()
            except:
                # Exclude unreadable files 
                self.report_load_errors.append(source_code_path)
                continue
            
            # Read comments in source codes
            comments = parser.c_comment_parser(source)
            # comments : original comment list
            _, words, _ = tokenizer.get_grams_from_source(comments)

            result_dict = {'name' : None, 'license' : None, 'index' : None}
            for index, word in enumerate(words):
                if tb_spdx_id.get(word) != None:
                    result_dict['name'] = source_code_path
                    result_dict['license'] = word
                    result_dict['index'] = index
                    self.report_spdx_licenses.append(result_dict)
                    break
                # Don't find license
            result_dict['name'] = source_code_path
            self.report_spdx_licenses.append(result_dict)

        return self.report_spdx_licenses, self.report_load_errors
        

    def copywrite_finder(self):
        pass


    def license_compatibility_check(self):
        pass


    

