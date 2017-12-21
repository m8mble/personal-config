#!/usr/bin/env python3

import argparse
import pathlib
import subprocess


class Installer:
    def __init__(self):
        self.done = set() # set of installers already executed
        self.backup_dir = pathlib.Path.cwd() / 'backup' # where we save conflicting files

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

    def _link_config(self, src, tgt):
        # Save conflicts if any
        if tgt.exists() and tgt.resolve() != src:
            print('   {:} exists; saving backup.'.format(tgt))
            self.backup_dir.mkdir(parents=False, exist_ok=True)
            tgt.rename(self.backup_dir / tgt.name)
        # Ensure link (if not already ok)
        if not tgt.exists():
            tgt.symlink_to(src)


    @depends_on('powerline', 'vundle')
    def setup_vim(self):
        print('Setting up VIM')
        # TODO Ensure vim is actually installed
        # TODO Link vim config
        # TODO Install plugins
        # TODO powerline vim config

    @depends_on()
    def setup_powerline(self):
        print('Updating powerline')
        subprocess.check_call('pip install --user --upgrade powerline-status'.split())

        # Get powerline fonts
        font_repo = pathlib.Path.home() / 'software' / 'powerline-fonts'
        font_repo.mkdir(parents=True, exist_ok=True)
        if (font_repo / '.git').exists():
            print('Updating powerline fonts')
            subprocess.check_call('git pull'.split(), cwd=font_repo)
        else:
            print('Cloning powerline fonts')
            subprocess.check_call('git clone --depth=1 https://github.com/powerline/fonts.git'.split() + [str(font_repo)])

        print('Installing powerline fonts')
        subprocess.check_call('bash install.sh'.split(), cwd=font_repo)

        print('Setting up powerline config')
        self._link_config(pathlib.Path.cwd() / 'powerline', pathlib.Path.home() / '.config' / 'powerline')

        #TODO remainder of https://askubuntu.com/questions/283908/how-can-i-install-and-use-powerline-plugin

    @depends_on()
    def setup_vundle(self):
        print('Setting up vundle')

    @depends_on('powerline')
    def setup_bash(self):
        print('Setting up bash config')
        self._link_config(pathlib.Path.cwd() / 'bash' / 'bashrc', pathlib.Path.home() / '.bashrc')


####################################################################################


def _load_parser():
    parser = argparse.ArgumentParser(description='Create my favorite environment.')
    parser.add_argument('--vim', help='Setup vim config.', action='store_true')
    parser.add_argument('--bash', help='Setup bash config.', action='store_true')
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

