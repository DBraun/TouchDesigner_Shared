import glob
import re

from os import path

import argparse

import sys
import time
import logging
import watchdog
from watchdog.observers import Observer
from watchdog.events import *

from ctypes import windll

ALLOWONDONE = False # ALLOW ON DONE. Boolean to allow special thing when queue becomes emtpy

def is_file_copy_finished(file_path):
    finished = False

    GENERIC_WRITE         = 1 << 30
    FILE_SHARE_READ       = 0x00000001
    OPEN_EXISTING         = 3
    FILE_ATTRIBUTE_NORMAL = 0x80

    if not isinstance(file_path, str):
        file_path_unicode = file_path.decode('utf-8')
    else:
        file_path_unicode = file_path

    h_file = windll.Kernel32.CreateFileW(file_path_unicode, GENERIC_WRITE, FILE_SHARE_READ, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)

    if h_file != -1:
        windll.Kernel32.CloseHandle(h_file)
        finished = True

    # print('is_file_copy_finished: ' + str(finished))
    return finished

def wait_for_file_copy_finish(file_path):
    while not is_file_copy_finished(file_path):
        time.sleep(0.2)

def convert_movie(inputpath):

	print('pretending to do something with file: ' + str(inputpath))
	time.sleep(3)
	print('done with file : ' + str(inputpath))

class CustomFileEventHandler(watchdog.events.FileSystemEventHandler):

	def __init__(self):

		self.file_dict = {}

	def on_created(self, event):

		global ALLOWONDONE

		if isinstance(event, FileCreatedEvent):
			filename = event.src_path # gets the path of the modified file
			ALLOWONDONE = True
			wait_for_file_copy_finish(filename)
			# convert the movie
			convert_movie(filename)


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Watchdog for files appearing in a folder.')
    parser.add_argument('--path', type=dir_path)

    return parser.parse_args()

if __name__ == "__main__":

    parsed_args = parse_arguments()

    # watchdog start
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # event_handler = LoggingEventHandler()
    event_handler = CustomFileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, parsed_args.path, recursive=True)
    observer.start()
    print('watching folder: ' + parsed_args.path)
    try:
        while True:
            if observer.event_queue.empty() and ALLOWONDONE:
                ALLOWONDONE = False
                print('queue became empty!')

            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    # watchdog end
