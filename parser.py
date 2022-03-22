import os, sys, json, re

KEYWORD_SET = './keywords.json'

class Parser:
    def __init__(self):
        self.keyworkd_set = json.loads(open(KEYWORD_SET,'r').read())

    def c_comment_parser(self, source):
        regrex = r'(//[^\n]*|/\*.*?\*/)'
        comments = re.findall(regrex, source, re.MULTILINE | re.DOTALL)
        return comments

    def shell_comment_parser(self, source):
        pass


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

    print()
    for i in blocks:
        print(i)

    #print(source)

    print()


if __name__ == '__main__':
    main()