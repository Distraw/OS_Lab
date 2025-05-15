import threading
import resource

if __name__ == '__main__':
    soft, hard = resource.getrlimit(resource.RLIMIT_NPROC)
    print(hard, soft)