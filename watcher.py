import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hmr
import re

TSTAMP = time.time()


class Watcher:
    DIRECTORY_TO_WATCH = "D:/GAMES/STEAM/steamapps/common/DARK SOULS III/Game/my_mod"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        else:
            reloadRegexps = [
                '\.msb.dcx.prev',
                '\.emevd'
            ]
            print(f'Changes on file {event.src_path}')
            global TSTAMP
            current_tstamp = time.time()
            tstamp_delta = current_tstamp - TSTAMP
            print(f'Modification delta: {tstamp_delta} seconds')
            for regex in reloadRegexps:
                regex = re.compile(regex)
                if (re.findall(regex, event.src_path) and tstamp_delta > 2):
                    hmr.reloadMap()
                    TSTAMP = time.time()
                    return
