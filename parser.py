import os
import sys
import json
import re
import itertools
import pandas as pd

KEYWORD_SET = './keywords.json'
SPDX_LICENSES = '/home/moonsun/spdx_project/spdx_license/'

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
            read = json.load(open(path+license, 'r'))

            template = dict()
            elems = ['licenseId', 'name', 'licenseText', 'standardLicenseHeader']
            for tag in elems:
                try:
                    template[tag] = re.sub(r'\s\s+', ' ', read[tag]).replace('\n','')
                except:
                    template[tag] = None
            license_list.append(template)
        
        return license_list

    def gen_spdx_license_database(self):
        pass


class Tokenizer:
    def __init__(self):
        pass

    def get_grams(self, comments):
        grams = list()
        for comment in comments:
            # remove whitespace (2 more)
            comment = re.sub(r'\s\s+', ' ', comment)
            words = comment.split(' ')
            grams.extend(list(zip(words, words[1:])))
        
        return grams

class TokenComapre:
    def __init__(self):
        pass

    def lcs_lens(self, xs, ys):
        curr = list(itertools.repeat(0, 1 + len(ys)))
        for x in xs:
            prev = list(curr)
            for i, y in enumerate(ys):
                if x == y:
                    curr[i + 1] = prev[i] + 1
                else:
                    curr[i + 1] = max(curr[i], prev[i + 1])
        return curr

    def lcs(self, xs, ys):
        nx, ny = len(xs), len(ys)
        if nx == 0:
            return []
        elif nx == 1:
            return [xs[0]] if xs[0] in ys else []
        else:
            i = nx // 2
            xb, xe = xs[:i], xs[i:]
            ll_b = self.lcs_lens(xb, ys)
            ll_e = self.lcs_lens(xe[::-1], ys[::-1])
            _, k = max((ll_b[j] + ll_e[ny - j], j)
                        for j in range(ny + 1))
            yb, ye = ys[:k], ys[k:]

            return self.lcs(xb, yb) + self.lcs(xe, ye)

    def lcs_similarity(self, xs, ys):
        output = self.lcs(xs, ys)

        try:
            simularity = len(output) / max(len(xs), len(ys))
        except:
            simularity = 0

        return simularity

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

    output = parser.spdx_license_loader()
    print()

    tokenizer = Tokenizer()
    grams = tokenizer.get_grams(blocks)

    token_compare = TokenComapre()
    lcs_score = token_compare.lcs_similarity(grams, grams)



if __name__ == '__main__':
    main()