# Overwrite default coloring
__git_ps1_colorize_gitstring ()
{
   local bad_color="${BIRed}"
   local warn_color="${Purple}"
   local ok_color="${Yellow}"
   local reset_color="${Color_Off}"

   local branch_color="${ok_color}"
   # Stashed content or Untracked Files
   if [ -n "${s}" ] || [ -n "${u}" ]; then
      branch_color="${warn_color}"
   fi
   # Modifications or detached
   if [ "${w}" = "*" ] || [ -n "${i}" ] || [ "${detached}" != "no" ]; then
      branch_color="$bad_color"
   fi

   c="$branch_color$c"
   z="${reset_color}$z${branch_color}"
   r="${reset_color}$r"
}

# Various variables you might want for your PS1 prompt instead
Time12h="\T"
Time12a="\@"
PathShort="\w"
PathFull="\W"
NewLine="\n"
Jobs="\j"
Date="\D{%d.%m.%y}"
User="\u"
Host="\h"


