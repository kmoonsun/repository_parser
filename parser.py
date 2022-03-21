import os, sys

root_directory = sys.argv[1]

file_list = list()
for root, dirs, files in os.walk(root_directory):
    for file in files:
        ext = os.path.splitext(file)[-1].split('.')[-1]
        if ext == '':
            print('none')
        print(ext)
        file_list.append(root+'/'+file)    

with open(file_list[0], 'r') as fp:
    source = fp.read()

print(source)