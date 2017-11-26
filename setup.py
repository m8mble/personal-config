#!/usr/bin/env python3

import argparse
import subprocess


class Installer:
    def __init__(self):
        self.done = set() # set of installers already executed

    def setup(self, *steps):
        """ Setup main method: Calls setup_* handlers for specified steps.
        """
        for step in steps:
            getattr(self, 'setup_{:}'.format(str(step)))()

    def depends_on(*requirements):
        """ Builds decorator that ensures setup for requirements.
        """
        def decorator(installer):
            def wrapper(self):
                self.setup(*requirements) # First our requirements
                if installer.__name__ not in self.done: # Now actual work iff needed
                    installer(self)
                    self.done.add(installer.__name__)
            return wrapper
        return decorator

    @depends_on('powerline', 'vundle')
    def setup_vim(self):
        print('Setting up VIM')
        # TODO Ensure vim is actually installed
        # TODO Link vim config
        # TODO Install plugins
        # TODO powerline vim config

    @depends_on()
    def setup_powerline(self):
        print('Setting up powerline')
        subprocess.check_call('pip install --user --upgrade powerline-status'.split())
        # TODO powerline fonts
        # -- remainder of https://askubuntu.com/questions/283908/how-can-i-install-and-use-powerline-plugin

    @depends_on()
    def setup_vundle(self):
        print('Setting up vundle')


####################################################################################


def _load_parser():
    parser = argparse.ArgumentParser(description='Create my favorite environment.')
    parser.add_argument('--vim', help='Setup vim config.', action='store_true')
    return parser

def _parse_cmdline():
    # Parse cmdline
    args = vars(_load_parser().parse_args())
    # Enable all parts by default ie. if nothing was selected
    if not any(args.values()):
        args.update({step: True for step in args.keys()})
    return args

def _main():
    # TODO:
    # -- xdg config: link config to ~/.config/user-dirs.dirs and call xdg-user-dirs-update
    # -- bashrc
    # -- .profile
    args = _parse_cmdline()
    Installer().setup(*[k for k, v in args.items() if v])

if __name__ == '__main__':
    _main()

