import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hmr
import re
import json


class Watcher:

    def __init__(self):
        self.observer = Observer()
        with open("config.json", "r") as read_file:
            self.config = json.load(read_file)

    def run(self):
        event_handler = Handler(self.config)
        self.observer.schedule(
            event_handler, self.config['mod_dir'], recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()

        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config
        self.tstamp = time.time()

    def on_any_event(self, event):
        if event.is_directory:
            return None

        else:
            print(f'Changes on file {event.src_path}')
            current_tstamp = time.time()
            tstamp_delta = current_tstamp - self.tstamp
            print(f'Reload delta: {tstamp_delta} seconds')
            for regex in self.config['reload_regexps']:
                regex = re.compile(regex)
                if (re.findall(regex, event.src_path) and tstamp_delta > 2):
                    hmr.reloadMap()
                    self.tstamp = time.time()
                    return
