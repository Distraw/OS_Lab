import psutil
import argparse

def get_process_info(proc):
    try:
        parent_pid = proc.ppid()
        cmdline = ' '.join(proc.cmdline()) if proc.cmdline() else 'no_command_line'
        print('ID: ', proc.pid, '\tParent ID:', parent_pid, '\tCMD: ', cmdline)
    except psutil.NoSuchProcess:
        print(proc.pid, ' does not exist. Skipping...')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--all", action="store_true", help="Show information about all running processes")
    args = parser.parse_args()

    if args.all:
        for process in psutil.process_iter(attrs=['pid']):
            get_process_info(process)
    else:
        get_process_info(psutil.Process())