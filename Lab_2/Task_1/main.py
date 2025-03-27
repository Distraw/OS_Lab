import stat
import os
import argparse
import pwd
import grp
import time


def list_catalog(path, arg_all, arg_long):
    try:
        file = os.listdir(path)
        if not arg_all:
            file = [f for f in file if (not f.startswith('.') and not f.startswith('..'))]

        if arg_long:
            for f in file:
                full_path = os.path.join(path, f)
                file_stat = os.stat(full_path)

                file_type = 'd' if os.path.isdir(full_path) else os.path.splitext(full_path)[1]
                file_perm = stat.filemode(file_stat.st_mode)

                file_owner = pwd.getpwuid(file_stat.st_uid).pw_name
                file_group = grp.getgrgid(file_stat.st_gid).gr_name

                file_hard_links = file_stat.st_nlink
                file_size = file_stat.st_size if not os.path.isdir(full_path) else get_dir_size(full_path)
                mod_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_stat.st_mtime))

                print(f, file_type, file_perm, file_owner, file_group, file_hard_links, file_size, mod_time)
        else:
            for f in file:
                print(f)
    except Exception as e:
        print(e)

def get_dir_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('wd', nargs='?', default=os.getcwd(), metavar='path', help='Path to directory to analyze')
    parser.add_argument('-a', '--all', action='store_true', help='Show hidden files/directories')
    parser.add_argument('-l', '--long', action='store_true', help='Show additional info about files/directories')

    args = parser.parse_args()

    list_catalog(args.wd, args.all, args.long)