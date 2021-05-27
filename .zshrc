# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="spaceship"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in ~/.oh-my-zsh/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to automatically update without prompting.
# DISABLE_UPDATE_PROMPT="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS=true

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
	git
	alias-finder
	# notify
	zsh-autosuggestions
	zsh-syntax-highlighting
# 	history-substring-search
)

ZSH_ALIAS_FINDER_AUTOMATIC=true

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"


# postgres

alias pg_start="launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist"
alias pg_stop="launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist"

# Open Webstorm - workaround for new projects not launching in webstorm when using web storm terminal command
# Opens current directory in webstorm
alias webstorm="open -a /Applications/WebStorm.app ."
alias xcode="open -a /Applications/Xcode.app ."

# GitHub CLI

alias pr:merge="gh pr merge -m -d && gl"

# git clone here

gch() {
isOpenInWebstorm=false
folderName=""
ssh=""
while getopts ":w" opt; do
          case $opt in
            w)
              isOpenInWebstorm=true
              ;;
            \?)
              ;;
          esac
        done
if [ "$isOpenInWebstorm" = true ] ;
then
    folderName="$2"
    ssh="$3"
else
    folderName="$1"
    ssh="$2"
fi
if [ "$folderName" != "" ] ;
then
    mkdir "$folderName"
else
    echo "Missing folder name"
    exit 1
fi
cd "$folderName"
if [ "$ssh" != "" ] ;
then
  git clone "$ssh" .
else
  echo "Please enter an SSH"
  exit 1
fi
if [ "$isOpenInWebstorm" = true ] ;
then
    webstorm
fi
}

# checkout new branch

cnb() {

if [ "$1" != "" ]
then
	git checkout -b "$1"
else
	echo Please enter a branch name
fi
}

grfb() {
if [ "$1" != "" ]
then
	if [ "$2" != "" ]
	then
	gco "$2"
	else
	echo please enter a base branch name
	fi
	git pull origin "$2" --rebase
	gco "$1"
	git rebase "$2"
else
	echo Please enter the name of the branch to be rebased
fi
}

# bump-to-latest

bump() {
if [ "$1" != "" ]
then
	if [ "$2" != "" ]
	then
		npm uninstall "$2" && npm i --save "$2"@"$1"
	else
	echo please provide a package name
	fi
else
	echo Please provide a version tag
fi
}


# bump-to-latest

bump-dev() {
if [ "$1" != "" ]
then
	if [ "$2" != "" ]
	then
		npm uninstall "$2" && npm i --save-dev "$2"@"$1"
	else
	echo please provide a package name
	fi
else
	echo Please provide a version tag
fi
}

# aliases
alias gs="git status"
alias rsb="npm uninstall wwu-storybook"
alias asb="npm i --save wwu-storybook"
alias asbc="npm uninstall wwu-storybook && npm i --save wwu-storybook@canary"
alias afc="npm uninstall wwu-formio && npm i --save wwu-formio@canary"

# browserstack

export BROWSERSTACK_USER="chriskay2"
export BROWSERSTACK_KEY="keghnhNtSKeoukaqtmyE"

pr:create() {
if [ "$1" != "" ]
then
	gh pr create -t "$1" -b "$2"
else
	echo Please provide a PR title
fi
}

yt () {
if [ -f "$2" ]
then
echo Please provide a YouTube URL

else
while getopts ":a:v" opt; do
  case $opt in
    a)
      youtube-dl --extract-audio --audio-format mp3 "$2"
      ;;
    v)
      youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' "$2"
      ;;
    \?)
      echo "Unsupported option" >&2
      exit 1
      ;;
  esac
done
fi
}

spotify() {
if [ -f "$1" ]
then
echo Please provide an artist name
exit 1
fi
if [ -f "$2" ]
then
echo Please provide an album name
exit 1
fi
if [ -f "$3" ]
then
echo Please provide a YouTube URL
exit 1
fi
mkdir "$1" && cd "$1"
mkdir "$2" && cd "$2"
yt -a "$3"
}

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
