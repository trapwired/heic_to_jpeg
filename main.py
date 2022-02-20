import os
import shutil
import sys
import time
import logging

from wand.image import Image

COUNT = 0
TOTAL = 7639    # Total number of Objects in src folder, only used for progress message

# now we will Create and configure logger
logging.basicConfig(filename="std.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec))


def convert_heic(src, dst):
    img = Image(filename=src)
    img.format = 'jpg'
    img.save(filename=dst)
    img.close()


def walk_it(src, dst):
    global COUNT
    if not os.path.exists(dst):
        os.makedirs(dst)
    ll = os.listdir(src)
    for node in ll:
        COUNT += 1
        new_path_src = os.path.join(src, node)
        new_path_dst = os.path.join(dst, node)
        node_name = node.split('.')[0]
        if os.path.isdir(new_path_src):
            logger.info(str(COUNT) + ': Traversing: ' + new_path_src)
            sys.stdout.write('\r' + "{0}/{1} - Dir  - {2}".format(COUNT, TOTAL, new_path_src))
            sys.stdout.flush()
            walk_it(new_path_src, new_path_dst)
        elif os.path.isfile(new_path_src):
            sys.stdout.write('\r' + "{0}/{1} - File - {2}".format(COUNT, TOTAL, new_path_src))
            sys.stdout.flush()
            logger.info(str(COUNT) + ': Processing: ' + new_path_src)
            if node.endswith(('.heic', '.HEIC')):
                convert_heic(new_path_src, os.path.join(dst, node_name + '_1.jpg'))
            else:
                shutil.copy(new_path_src, new_path_dst)


if __name__ == '__main__':
    start_time = time.time()
    walk_it('/Path/to/Source/Folder', '/Path/To/Output/Folder')
    end_time = time.time()
    time_lapsed = end_time - start_time
    print()
    time_convert(time_lapsed)
