import threading

class FileReaderThread(threading.Thread):
    def __init__(self, file : str):
        super().__init__()
        self._file = file
        self._content = None

    def run(self):
        self.read()

    def read(self):
        with open(self._file, 'r', encoding='utf-8') as f:
            self._content = f.read()

    def get_content(self):
        return self._content

if __name__ == '__main__':
    reader_thread = FileReaderThread('./information.txt')
    reader_thread.start()

    reader_thread.join()
    print(reader_thread.get_content())