# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="/Users/barcld01/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="robbyrussell"

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
plugins=( git alias-finder notify zsh-autosuggestions zsh-syntax-highlighting history-substring-search)

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

  # Set Spaceship ZSH as a prompt
  autoload -U promptinit; promptinit
  prompt spaceship


# morph modules set up
alias mpm="npm --registry https://npm.morph.int.tools.bbc.co.uk --cert=\"$(cat /etc/pki/certificate.pem)\" --key=\"$(cat /etc/pki/certificate.pem)\" --cafile=/etc/pki/tls/certs/ca-bundle.crt"

# postgres

alias pg_start="launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist"
alias pg_stop="launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist"

# git clone here

gch() {

if [ "$1" != "" ]
then
	mkdir "$1"
fi
	cd "$1"
    if [ "$2" != "" ]
    then
        git clone "$2" .
    else
        echo Please enter an SSH
    fi
}

# change name here - for changing git authoring

cnh() {

if [ "$1" != "" ]
then
	mkdir "$1"
fi
	cd "$1"
    if [ "$2" != "" ]
    then
        git clone "$2" .
    else
        echo Please enter an SSH
    fi
git filter-branch --env-filter '

OLD_EMAIL="daniel@urbanintel.io"
CORRECT_NAME="Daniel Barclay"
CORRECT_EMAIL="barclaysd@me.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags

git push origin +master
cd ..
rm -rf "$1"
}

# dev certs for mozart
export DEV_CERT_PEM="/etc/pki/certificate.pem"
export DEV_CA_PEM="/etc/pki/cloud-ca.pem"

# checkout new branch

cnb() {

if [ "$1" != "" ]
then
	git checkout -b "$1"
else
	echo Please enter a branch name
fi
}

# rebase feature branches from a main branch
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

# aliases
alias gs="git status"
# uninstall storybook
alias rsb="npm uninstall wwu-storybook"
# add storybook canary
alias asbc="npm i --save wwu-storybook"

# migrate from bitbucket to GitHub

mtg() {
if [ "$1" != "" ]
then
	gch "$1" "$2"
	git remote add upstream "$3"
	git push upstream master
	git push origin --all
	git push --tags upstream
	cd ..
	rm -rf "$1"
fi
}

export PATH="/usr/local/opt/postgresql@10/bin:$PATH"

# chromedriver versioning
export PATH=$PATH:~/.bin
WEBDRIVER_DRIVER_VERSION=$(chromedriverversion.sh)

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="/Users/barcld01/.sdkman"
[[ -s "/Users/barcld01/.sdkman/bin/sdkman-init.sh" ]] && source "/Users/barcld01/.sdkman/bin/sdkman-init.sh"
