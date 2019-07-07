########################################################################################################################
# General

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

export LD_LIBRARY_PATH="${HOME}/.local/lib/:${HOME}/software/lib64/:${LD_LIBRARY_PATH}"
export PATH="${HOME}/bin:${HOME}/.local/bin:${HOME}/software/bin:/usr/local/bin:/usr/local/opt/ncurses/bin:${PATH}"

export EDITOR=nvim


########################################################################################################################
# Aliases

if [[ "$(uname -s)" == "Darwin" ]]
then
   # Favor GNU originals provided by brew's coreutils package
   alias readlink='greadlink'
   alias dircolors='gdircolors'
   LS='gls'
   alias ls="${LS}"
else
   LS='ls'
fi

# ls helpers
alias lr="${LS} -ltrah --color=auto"
alias ll="${LS} -lah --color=auto"

# Create directory and enter it
function mkcd() { mkdir -p "${@}" && cd "${_}"; }


########################################################################################################################
# Development
UBSAN_OPTIONS=print_stacktrace=1


########################################################################################################################
# Source local overwrites if present
BASHRC_LOCAL="${HOME}/.profile.local"
if [ -f "${BASHRC_LOCAL}" ]
then
    source "${BASHRC_LOCAL}"
fi

