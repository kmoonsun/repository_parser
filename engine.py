import json

class Engine:
    spdx_licenses = list()
    load_errors = list()
    copyrights = list()
    # interface에 구현한 탐색 알고리즘 옮겨 담기 해야함.
    def __init__(self, database_path):
        self.spdx_license_database = list(json.loads(open(database_path,'r').read()))
        self.spdx_license_id_database = [list(i.keys())[0] for i in self.spdx_license_database]
        
        # Generate spdx_id hashtable
        self.tb_spdx_id = dict()
        for i in self.spdx_license_id_database:
            self.tb_spdx_id[i] = 0


    def spdx_licese_finer(self):
        pass

    def copywrite_finder():
        pass