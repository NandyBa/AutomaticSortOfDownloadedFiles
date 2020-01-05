#!/usr/bin/env python
import config as cfg
import os
import re
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

track_dir = cfg.path['download']+'/'

audio_regex_list = ["mp3", "wav", "m3u"]
text_regex_list = ["txt", "doc", "docx", "odt", "pdf", "tex", "epub"]

Files_moved = []

def main():
    print("Downloads folder organizer")
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, track_dir)
    my_observer.start()
    try:
         while True:
             time.sleep(1)
    except KeyboardInterrupt:
         my_observer.stop()
         my_observer.join()

def sort_file(file):
	global Files_moved
	path, filename = file.rsplit('/', 1)
	

	file_extension = filename.rsplit('.', 1)[1]
	if(not(filename in Files_moved) and file_extension != 'tmp' ):
		print(filename + " has been detected")
        while(os.path.isfile(file) == False):
            time.sleep(1)
            
		if(file_extension in audio_regex_list):
			move_file(filename, path, cfg.path['music'])
		elif(file_extension in text_regex_list):
			move_file(filename, path, cfg.path['document'])
	

def on_created(event):
    file = event.src_path
    sort_file(file)

def move_file(filename, oldPath, newPath):
	global Files_moved
	Files_moved = Files_moved + [filename]
	Path(oldPath + "/" + filename).rename(newPath + "/" + filename)
	print(filename + " has been moved")


main()


