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
        subprocess.call(['bash', 'install.sh']) # run app
        return get_sha()

def launch(*args):
    print('Launching {}'.format(args))
    url    = args[0]
    appDir = args[1]
    handle = None
    app_sha = get_app_sha(appDir)
    sha     = get_sha()
    last    = time.time()

    try:
        print('Waiting.', end='')
        while True:
            current = time.time()
            if current - last > updateInterval:
                last = current
                print('Checking for updates..')
                new_app_sha = update(url, appDir)
                print('Pulling backbone')
                subprocess.call(['git', 'pull']) # pull backbone's code
                new_sha = get_sha()
                if app_sha != new_app_sha:
                    print('Updating app')
                    # If our app has updated, restart it
                    print('Re-running..')
                    if handle is not None:
                        print('Killing..')
                        handle.kill()
                        with directory(appDir):
                            handle = subprocess.Popen(['bash', 'run.sh'])
                    app_sha = new_app_sha
                elif sha != new_sha:
                    print('Backbone updated...')
                    #if handle is not None:
                    #    print('Killing..')
                    #    handle.kill()
                    #print('Updating backbone')
                    ## If backbone has updated, restart
                    #subprocess.call(['./backbone'] + args)
                    #return 0
                if handle is None:
                    with directory(appDir):
                        handle = subprocess.Popen(['bash', 'run.sh'])
                print('Waiting.', end='')
            else:
                print('.', end='', flush=True)
                time.sleep(waitInterval)
        return 0
    finally:
        if handle is not None:
            print('Killing..')
            handle.kill()

if __name__ == '__main__':
    sys.exit(launch(sys.argv[1:]))
