########################################################################################################################
# General

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

export LD_LIBRARY_PATH="${HOME}/.local/lib/:${HOME}/software/lib64/:${LD_LIBRARY_PATH}"
export PATH="${HOME}/bin:${HOME}/.local/bin:${HOME}/software/bin:/usr/local/bin:/usr/local/opt/ncurses/bin:${PATH}"

export EDITOR=nvim


########################################################################################################################
# Application specific configurations

# Export rg configuration
function update_ripgreprc() {
   export RIPGREP_CONFIG_PATH="${HOME}/.ripgreprc"
   RIPGREP_MASTER_CONFIG="${RIPGREP_CONFIG_PATH}.master"
   RIPGREP_LOCAL_CONFIG="${RIPGREP_CONFIG_PATH}.local"

   # Check whether current config is up to date
   if [[    ( "${RIPGREP_CONFIG_PATH}" -nt "${RIPGREP_MASTER_CONFIG}" )
         && (   ( ! -f "${RIPGREP_LOCAL_CONFIG}" )
             || ( "${RIPGREP_CONFIG_PATH}" -nt "${RIPGREP_LOCAL_CONFIG}" ) ) ]];
   then
      # Config up to date
      return;
   fi

   # Start with master config; remove existing (potentially outdated)
   cat "${RIPGREP_MASTER_CONFIG}" > "${RIPGREP_CONFIG_PATH}"
   # Append local config (if any)
   if [ -f "${RIPGREP_LOCAL_CONFIG}" ]; then
      cat "${RIPGREP_LOCAL_CONFIG}" >> "${RIPGREP_CONFIG_PATH}"
   fi
}
update_ripgreprc


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
function rmkcd() { rm -rf "${@}" && mkcd "${@}"; }


########################################################################################################################
# Development
UBSAN_OPTIONS=print_stacktrace=1


########################################################################################################################
# Source local overwrites if present
PROFILE_LOCAL="${HOME}/.profile.local"
if [ -f "${PROFILE_LOCAL}" ]
then
    source "${PROFILE_LOCAL}"
fi

