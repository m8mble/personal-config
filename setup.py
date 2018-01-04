#!/usr/bin/env python3

import argparse
import glob
import os.path
import pathlib
import subprocess
import tempfile


class Installer:
    def __init__(self):
        self.done = set() # set of installers already executed

        self.install_source = pathlib.Path(__file__).parent.resolve()
        self.backup_dir = self.install_source / 'backup' # where we save conflicting files
        self.vim_bundle = pathlib.Path.home() / '.vim' / 'bundle'  # home to vim plugins

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
                    print('Installing {:}'.format(installer.__name__.replace('setup_', '').replace('_', '-')))
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
            tgt.symlink_to(os.path.relpath(src, start=tgt.parent))

    @staticmethod
    def _update_git(src, tgt):
        if tgt.exists():
            subprocess.check_call(['git', 'pull'], cwd=tgt)
        else:
            subprocess.check_call(['git', 'clone', src, tgt])

    @depends_on('vim_pathogen', 'vim_powerline', 'vim_colors_solarized')
    def setup_vim(self):
        # TODO Ensure vim is actually installed
        local = self.install_source / 'vim'
        installed = pathlib.Path.home() / '.vim'
        self._link_config(local / 'vimrc', installed / 'vimrc')
        # TODO Link vim config
        # TODO powerline vim config

    @depends_on()
    def setup_powerline(self):
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
        self._link_config(self.install_source / 'powerline', pathlib.Path.home() / '.config' / 'powerline')

        #TODO remainder of https://askubuntu.com/questions/283908/how-can-i-install-and-use-powerline-plugin

    @depends_on()
    def setup_vim_pathogen(self):
        self.vim_bundle.mkdir(exist_ok=True, parents=True)
        autoload = self.vim_bundle.parent / 'autoload'
        autoload.mkdir(exist_ok=True, parents=True)

        install = self.vim_bundle / 'vim-pathogen'
        Installer._update_git('https://github.com/tpope/vim-pathogen.git', install)
        self._link_config(install / 'autoload' / 'pathogen.vim', autoload / 'pathogen.vim')

    @depends_on('vim_pathogen')
    def setup_vim_colors_solarized(self):
        Installer._update_git('git://github.com/altercation/vim-colors-solarized.git', self.vim_bundle / 'vim-colors-solarized')

    @depends_on('powerline')
    def setup_vim_powerline(self):
        installs = glob.glob(str(pathlib.Path.home() / '.local' / '**' / 'powerline' / 'bindings' / 'vim'), recursive=True)
        assert len(installs) == 1, 'Can\'t select among powerline installs {:}'.format(installs)
        self._link_config(pathlib.Path(installs[0]), self.vim_bundle / 'vim-powerline')

    @depends_on('powerline', 'dircolors', 'kde')
    def setup_bash(self):
        self._link_config(self.install_source / 'bash' / 'bashrc', pathlib.Path.home() / '.bashrc')

    def setup_kde(self):
        search = pathlib.Path.home() / '.kde*' / 'share' / 'apps' / 'konsole' / 'Solarized*.colorscheme'
        if not glob.glob(str(search)):  # Check that we didn't install already
            with tempfile.TemporaryDirectory() as workarea:
                git_tgt = pathlib.Path(workarea).resolve() / 'kde-colors-solarized'
                Installer._update_git('https://github.com/hayalci/kde-colors-solarized.git', git_tgt)
                subprocess.check_call(['bash', 'install.sh'], cwd=git_tgt)

    def setup_dircolors(self):
        install_dir = pathlib.Path.home() / '.config' / 'dircolors-solarized'
        Installer._update_git('https://github.com/seebi/dircolors-solarized.git', install_dir)
        self._link_config(install_dir / 'dircolors.256dark', pathlib.Path.home() / '.dircolors')


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

