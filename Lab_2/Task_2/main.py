import argparse
import os

def has_hard_links(path):
    try:
        file_stat = os.stat(path)
        return file_stat.st_nlink > 1
    except FileNotFoundError:
        print('File ', path, ' not found')
        return False

def print_empty_files(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                full_path = os.path.join(dirpath, f)
                try:
                    if os.stat(full_path).st_size == 0 and not has_hard_links(full_path):
                        print(full_path)
                except FileNotFoundError:
                    print('File ', full_path, ' seems to be broken. Skipping...')


def print_empty_directories(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for d in dirnames:
            full_path = os.path.join(dirpath, d)
            if get_dir_empty(full_path):
                print(full_path)

def delete_empty_directories(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for d in dirnames:
            full_path = os.path.join(dirpath, d)
            if get_dir_empty(full_path):
                os.rmdir(full_path)
                print('Deleting ', full_path)


def get_dir_empty(path) -> bool:
    if not os.listdir(path):
        return True
    else:
        return False


def delete_empty_files(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            try:
                if os.stat(full_path).st_size == 0 and not has_hard_links(full_path):
                    os.remove(full_path)
                    print('Deleting ', full_path)
            except FileNotFoundError:
                print('File ', full_path, ' seems to be broken. Skipping...')
    print("Deletion completed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('wd', nargs='?', default=os.getcwd(), metavar='path', help='Path to directory to analyze')
    parser.add_argument('-lf', '--listfiles', action='store_true', help='Show empty files in sub- and directory')
    parser.add_argument('--deletefiles', action='store_true', help='Find and delete all empty files in sub- and directory')
    parser.add_argument('-ld', '--listdirs', action='store_true', help='Show empty dirs in sub- and directory')
    parser.add_argument('--deletedirs', action='store_true', help='Find and delete all empty dirs in sub- and directory')

    args = parser.parse_args()

    if args.listfiles:
        print_empty_files(args.wd)

    if args.deletefiles:
        print('Are you sure you want to delete all empty files in ', args.wd, ' and all subdirectories?')
        if input('Print \'Yes\' to continue: ') == 'Yes':
            delete_empty_files(args.wd)

    if args.listdirs:
        print_empty_directories(args.wd)

    if args.deletedirs:
        print('Are you sure you want to delete all empty directories in ', args.wd, ' and all subdirectories?')
        if input('Print \'Yes\' to continue: ') == 'Yes':
            delete_empty_directories(args.wd)