import os, sys

root_dir = sys.argv[1]

for root, dirs, files in os.walk(root_dir):
    print(root)