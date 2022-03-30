import json

class Engine:
    spdx_licenses = list()  # 식별된 sdpx 라이선스
    load_errors = list()    # 읽을 수 없는 파일 (소스코드 아님)
    copyrights = list()     # 저작권 표기 정보

    # interface에 구현한 탐색 알고리즘 옮겨 담기 해야함.
    def __init__(self, path):
        self.spdx_license_database = self.load_license_database_to_list(path)
        self.spdx_license_id_database = self.load_license_id_to_hashtable()
        
        # Init spdx_id hashtable
        self.tb_spdx_id = dict()
        for i in self.spdx_license_id_database:
            self.tb_spdx_id[i] = 0

    
    def load_license_id_to_list(self):
        return [list(i.keys())[0] for i in self.spdx_license_database]


    def load_license_database_to_list(self, path):
        return list(json.loads(open(path,'r').read()))


    def spdx_licese_finer(self):
        pass


    def copywrite_finder(self):
        pass


    def license_compatibility_check(self):
        pass


    

