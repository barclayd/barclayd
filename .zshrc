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
	zsh-autosuggestions
	zsh-syntax-highlighting
	history-substring-search
    notify
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

# Open Webstorm - workaround for new projects not launching in webstorm when using web storm terminal command
# Opens current directory in webstorm
alias webstorm="/usr/local/bin/webstorm ."
alias xcode="open -a /Applications/Xcode.app ."
alias openVPN="open -a /Applications/'OpenVPN Connect'.app"
alias docker="/Applications/Docker.app/Contents/Resources/bin/docker"


# file directory movements
function ..() {
    if [ $# -lt 1 ]; then
        cd ..
    else
        local re='^[0-9]+$'
        if [[ "$1" =~ $re ]] ; then
            for i in $(seq $1); do
                cd ..
            done
        else
            cd ..
        fi
    fi
}

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

# bump-to-latest

bump() {
version=""
package=""
isDevDependency=false

while getopts ":D" opt; do
          case $opt in
            D)
              isDevDependency=true
              ;;
          esac
        done
if [ "$isDevDependency" = true ] ;
then
    package="$2"
    version="$3"
else
    package="$1"
    version="$2"
fi
if [ "$version" = "" ] ;
then
    version="latest"
fi
if [ "$package" = "" ] ;
then
    echo "Missing package"
    exit 1
fi
if [ "$isDevDependency" = true ] ;
then
    npm uninstall "$package" && npm i -D "$package"@"$version"
else
    npm uninstall "$package" && npm i -S "$package"@"$version"
fi
}


# aliases
alias gs="git status"
alias guc="git reset --soft HEAD^"

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
      youtube-dl --add-header 'Cookie:' --extract-audio --audio-format mp3 "$2"
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
artist=""
album=""
title=""
youtubeURL=""
while getopts ":s" opt; do
          case $opt in
            s)
              title=$2
              album=$2
              artist="$3"
              youtubeURL="$4"
              ;;
            \?)
            echo "Unsupported option" >&2
            return
            ;;
          esac
        done
if [ "$1" != "-s" ]
then
    title=$1
    artist="$2"
    album="$3"
    youtubeURL="$4"
fi
if [ "$artist" = "" ]
then
echo Please provide the artist name
return
fi
if [ "$album" = "" ]
then
echo Please provide the album name
return
fi
if [ "$title" = "" ]
then
echo Please provide the song title
return
fi
if [ "$youtubeURL" = "" ]
then
echo Please provide a YouTube URL
return
fi
printf "\e\n[94mDownloading song from YouTube 🎵\n"
mkdir "$artist" && cd "$artist"
mkdir "$album" && cd "$album"
yt -a "$youtubeURL"
printf "\e\n[94mSong successfully downloaded! 🪄\n"
printf "\e\n[92mAdding to Spotify 🚀\n"
for file in *.mp3; do mv "$file" "$title.mp3" ; done
songId=${youtubeURL#*=}
kid3-cli -c "set title $title" \
         -c "set albumart 'https://img.youtube.com/vi/$songId/0.jpg'" \
         -c "set artist '$artist'" \
         -c "set album '$album'" \
         ./"$title.mp3"
cd ~
mv ~/"$artist"/ ~/Music/Music/Media.localized/Music/
cd ~/Music/Music/Media.localized/Music/"$artist"/"$album"
printf "\e\n[92m$title by $artist is ready on Spotify 💥\n"
}

gitPushEverything() {
currentBranchName=$(git rev-parse --abbrev-ref HEAD)
git push --set-upstream origin "$currentBranchName"
numberOfUnpushedCommits=$(git log @{u}.. 2>/dev/null | wc -l | xargs)
if [ "$numberOfUnpushedCommits" -gt 0 ] ;
then
  echo "Pushing up additional commits"
  HUSKY=0 git push --set-upstream origin "$currentBranchName"
fi
}

gpe() {
gitPushEverything
}

link() {
folderToCreateLocalPackage=""
folderToInstallLocalPackage=$(basename "$PWD")
isDevDependency=false
while getopts ":D" opt; do
          case $opt in
            D)
              isDevDependency=true
              ;;
          esac
        done
if [ "$isDevDependency" = true ] ;
then
    folderToCreateLocalPackage="$2"
else
    folderToCreateLocalPackage="$1"
fi
if [ "$folderToCreateLocalPackage" = "" ] ;
then
    echo "Missing folder name to create local package"
    return 1
fi
# rm -rf *.tgz 2>/dev/null
cd ../"$folderToCreateLocalPackage"
package=$(node -p "require('./package.json').name")
if [ "$package" = "" ] ;
then
    echo "Hmm... this doesn't look like a npm project. Check if you have a package.json in the root and try again"
    return 1
fi
npm pack
pathToParentRepo="../"
pathToInstallLocalPackage=$pathToParentRepo$folderToInstallLocalPackage
mv *.tgz ${pathToInstallLocalPackage}
cd "$pathToInstallLocalPackage"
if [ "$isDevDependency" = true ] ;
then
    npm uninstall "$package" && npm i -D *.tgz
else
    npm uninstall "$package" && npm i -S *.tgz
fi
}

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

autoload -U add-zsh-hook
load-nvmrc() {
  local node_version="$(nvm version)"

  local nvmrc_path="$(nvm_find_nvmrc)"

  if [ ! -f .nvmrc ]; then
      return
  fi

  local nvmrc_raw_version="$(head -n 1 .nvmrc)"

  if [ "$nvmrc_raw_version" = "__NODE_VERSION__" ]; then
    local node_version_from_package_json=$(node -p "require('./package.json').engines.node")

    nvm use "$node_version_from_package_json"

   elif [ -n "$nvmrc_path" ]; then
    local nvmrc_node_version=$(nvm version "$(cat "${nvmrc_path}")")

    if [ "$nvmrc_node_version" = "N/A" ]; then
      nvm install
    elif [ "$nvmrc_node_version" != "$node_version" ]; then
      nvm use
    fi
  elif [ "$node_version" != "$(nvm version default)" ]; then
    echo "Reverting to nvm default version"
    nvm use default
  fi
}
add-zsh-hook chpwd load-nvmrc
load-nvmrc


export NODE_EXTRA_CA_CERTS="/Users/Daniel.Barclay/combined_certs.pem"
export REQUESTS_CA_BUNDLE="/Users/Daniel.Barclay/combined_certs.pem"
export PATH="$HOME/.cargo/bin:$PATH"
export SPACESHIP_CONFIG="$HOME/.spaceshiprc.zsh"
