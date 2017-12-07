#!/usr/bin/env python3
import subprocess, time, sys, os
from contextlib import contextmanager

updateInterval = .1
waitInterval   = .1

@contextmanager
def directory(name):
    os.chdir(name)
    try:
        yield
    finally:
        os.chdir('..')

def get_sha():
    output = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
    return output.decode('utf-8').strip()

def get_app_sha(appDir):
    if not os.path.isdir(appDir):
        return None
    with directory(appDir):
        return get_sha()

def update(url, appDir):
    if not os.path.isdir(appDir):
        subprocess.call(['git', 'clone', url, appDir])
    with directory(appDir):
        print('Pulling app')
        subprocess.call(['git', 'pull'])        # pull app's code
        subprocess.call(['bash', 'install.sh']) # install app
        return get_sha()

def launch(*args):
    print('Launching {}'.format(args))
    url    = args[0]
    appDir = args[1]
    handle = None
    app_sha = None
    last    = time.time()

    try:
        print('Waiting.', end='')
        while True:
            current = time.time()
            if current - last > updateInterval:
                last = current
                print('Checking for updates..')
                new_app_sha = update(url, appDir)
                if handle is None:
                    with directory(appDir):
                        handle = subprocess.Popen(['bash', 'run.sh'])
                if app_sha != new_app_sha:
                    print('Updating app')
                    # If our app has updated, restart it
                    handle.kill()
                    with directory(appDir):
                        handle = subprocess.Popen(['bash', 'run.sh'])
                    app_sha = new_app_sha
            else:
                print('.', end='', flush=True)
                time.sleep(waitInterval)
        return 0
    finally:
        print('Killing..')
        handle.kill()

if __name__ == '__main__':
    sys.exit(launch(sys.argv[1:]))
