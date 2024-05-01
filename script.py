from threading import Thread
import os
import importlib.util
import sys
import time
import traceback
from shutil import copyfile
from modules.logging_colors import logger

dir_ = 'extensions/hot_reload'
dir_last_working = os.path.join(dir_, '.last_working')
os.makedirs(dir_last_working, exist_ok=True)


def modified(file):
    fp = os.path.join(dir_, file)
    return os.stat(fp).st_mtime


def reload(file, restore=False):
    name = file.rsplit('.', 1)[0]
    if restore:
        fp = os.path.join(dir_last_working, file)
    else:
        fp = os.path.join(dir_, file)

    spec = importlib.util.spec_from_file_location(f"reloadable_{name}", fp)
    reloadable = importlib.util.module_from_spec(spec)
    sys.modules[f"reloadable_{name}"] = reloadable
    spec.loader.exec_module(reloadable)


def backup(file):
    copyfile(os.path.join(dir_, file), os.path.join(dir_last_working, file))


def import_loop():
    last_modified = {}

    while True:
        time.sleep(2)

        for file in os.listdir(dir_):
            if file in ['script.py', 'utils.py']:
                continue

            if not file.endswith('.py'):
                continue

            modified_time = modified(file)
            delta = modified_time - last_modified.get(file, 0)
            if delta >= 0.5:

                logger.info(f'[HotReload]: Reloading {file!r}')
                last_modified[file] = modified_time

                try:
                    reload(file)
                    backup(file)
                    logger.debug('[HotReload]: Done')
                except Exception as e:
                    logger.warning(f'[HotReload]: Failed to load {file!r}')

                    print(traceback.format_exc())
                    print()
                    print(e)

                    try:
                        reload(file, restore=True)
                    except Exception:
                        pass
                    logger.info(f'[HotReload]: Restored {file!r} from last working backup')


def setup():
    Thread(target=import_loop, daemon=True).start()
