#!/usr/bin/python3
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import logging
from systemd.journal import JournalHandler

log = logging.getLogger('tmpwatcher')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)
log.info("sent to journal")


def on_created(event):
   print(f'event type: {event.event_type}  path : {event.src_path}')


if __name__ == "__main__":
   patterns = "*restart"
   ignore_patterns = ""
   ignore_directories = False
   case_sensitive = False
   my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
   my_event_handler.on_created = on_created
   path = "/tmp/"
   go_recursively = False
   my_observer = Observer()
   my_observer.schedule(my_event_handler, path, recursive=go_recursively)
   my_observer.start()
   try:
      while True:
         time.sleep(3)
   except KeyboardInterrupt:
      my_observer.stop()
      my_observer.join()
