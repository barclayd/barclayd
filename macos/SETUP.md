# Documented Steps for an Opinionated MacBook Configuration

## 1. Initial Setup

### Clone Repository
```shell
git clone https://github.com/barclayd/barclayd
```

### System Preferences
- Mission Control => Hot corners - bottom right = 'Put Display to Sleep'
- Siri => Enable Siri
- Desktop & Screen Saver => start after: Never
- Sharing => Rename Computer Name
- General => Appearance Auto

### Configuration Files
```shell
# Setup .zshrc and Brewfile tracking
ln -s ~/<PATH_TO_THIS_REPO>/.zshrc ~/.zshrc
ln -s ~/<PATH_TO_THIS_REPO>/.spaceshiprc.zsh ~/.spaceshiprc.zsh
ln -s ~/<PATH_TO_THIS_REPO>/macos/Brewfile ~/Brewfile

# Setup Git configuration
ln -s ~/<PATH_TO_THIS_REPO>/.gitignore ~/.gitignore_global
git config --global core.excludesfile ~/.gitignore_global
git config --global user.email barclaysd@me.com
git config --global user.name "Dan Barclay"
git config --global --add --bool push.autoSetupRemote true
git config --global merge.ff true
git config --global pull.ff only true
```

## 2. Development Environment

### Terminal Setup
#### Theme
Terminal -> Preferences -> Import -> ~/<PATH_TO_THIS_REPO>/macos/Terminal Theme/MaterialDarker.terminal

#### Homebrew
```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew bundle --file ~/Brewfile
```

#### Oh My Zsh & Plugins
```shell
# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install Spaceship Theme
git clone https://github.com/denysdovhan/spaceship-prompt.git "$ZSH_CUSTOM/themes/spaceship-prompt" --depth=1
ln -s "$ZSH_CUSTOM/themes/spaceship-prompt/spaceship.zsh-theme" "$ZSH_CUSTOM/themes/spaceship.zsh-theme"

# Install Powerline Fonts
git clone https://github.com/powerline/fonts.git --depth=1
cd fonts
./install.sh
cd ..
rm -rf fonts

# Install Zsh Plugins
git clone https://github.com/marzocchi/zsh-notify.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/notify
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

### Development Tools

#### Node.js
```shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
nvm install 16 --default

# NPM Configuration
echo "audit=false" >> ~/.npmrc
echo "fund=false" >> ~/.npmrc
```

#### Rust
```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# enter 1 when prompted
```

### GitHub Setup

#### SSH Configuration
```shell
ssh-keygen -t ed25519 -C "barclaysd@me.com"
pbcopy < ~/.ssh/id_ed25519.pub
# Add key to GitHub: https://github.com/settings/ssh/new
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

#### Multiple GitHub Accounts
Add to `~/.gitconfig`:
```
[include]
    path = ~/work.conf
[includeIf "gitdir:~/Documents/Coding/"]
    path = ~/personal.conf
```

Create configuration files:
```shell
# ~/work.conf
[user]
    email = <work email>
    name = Daniel Barclay

# ~/personal.conf
[user]
    email = barclaysd@me.com
    name = Daniel Barclay
[github]
    user = "barclayd"
[core]
    sshCommand = "ssh -i ~/.ssh/personal_github"
```

## 3. Applications

### Essential Apps
- ChatGPT
- 1Password
- Magnet
- HiddenBar
- CopyClip 2
- WhatsApp
- Spotify
- Signal
- Discord
- Figma
- Xcode
- SF Symbols

### Development Apps
- [Docker Desktop](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-arm64)
- Postman
- WebStorm
- Cursor
  * Change `workbench.activityBar.orientation` to `vertical`
  * Move activity bar to the right
  * Extensions:
    * Material Icon Theme
    * Material Theme - Free - Select Material Darker High Contrast
    * Open in Github
    * Open in Finder
    * Rainbow Tags
    * Intellij IDEA Keybindings
    * Markdown Preview Enhanced
    * Swift
    * Sweetpad


### WebStorm Configuration
#### Prettier
- Preferences => External Tools
- Import [Prettier tool](https://github.com/barclayd/barclayd/tree/master/webstorm/Prettier.xml)
- Setup key mapping
- Preferences => Prettier => Enable 'on code reformat' and 'on save'

#### ESLint
- Preferences => ESLint => Select 'automatic ESLint configuration'

### Chrome Extensions
- 1password
- Refined Github
- React Developer Tools
- Atom Material Icons
- Material Theme Collection

Configure Chrome DevTools:
- Preferences -> Theme -> Dark
- Experiments > "Allow extensions to load custom stylesheets"
- Devices > `Nexus 5`, `Nexus 5X`, `Pixel 4`, `iPhone 6/7/8 Plus`

### Chrome PWAs

- Google Maps
- X

### Slack
Theme:
```
#1A1A1A,#212121,#FF9800,#FFFFFF,#FF9800,#FFFFFF,#2EB67D,#FF9800,#1A1A1A,#727272
```

## 4. System Customization

### Finder
- Customize Toolbar
- Show Path Bar
- Add frequently used applications to sidebar

### Keyboard Shortcuts
- Launch Terminal: ⌘§
- Duplicate tab: <kbd>control</kbd> + <kbd>⇧</kbd> + <kbd>D</kbd>

### Other Utilities
```shell
# Smooth dock animation
remove_dock_animation_show_time.sh

# Show desktop icons if not visible
show_desktop_icons.sh
```
