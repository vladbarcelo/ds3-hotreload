import watcher
import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if not is_admin():
        input('Restart the program with admin privileges. ')
    else:
        w = watcher.Watcher()
        w.run()
