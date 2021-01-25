# Documented Steps for an Opinionated MacBook Configuration

```shell
git clone https://github.com/barclayd/barclayd
cd macos
```

### System Preferences

- Mission Control => Hot corners - bottom right = 'Put Display to Sleep'
- Siri => Enable Siri
- Desktop & Screen Saver => start after: Never
- Sharing => Rename Computer Name
- General => Appearance Auto

### Mac Apps

* [CopyClip](https://apps.apple.com/us/app/copyclip-clipboard-history/id595191960?mt=12)

#### Divvy

Setup global shortcuts

<p align="center">
<img width="75%" alt="Screenshot 2021-01-24 at 11 58 17" src="https://user-images.githubusercontent.com/39765499/105629561-9d4bbd00-5e3b-11eb-9a6d-4438be7501d8.png">
</p>

<p align="center">
<img width="75%" alt="Screenshot 2021-01-24 at 11 57 54" src="https://user-images.githubusercontent.com/39765499/105629564-a0df4400-5e3b-11eb-913f-705e5fabeb4e.png">
</p>

- To start automatically on login: System Preferences => Users & Groups => Login Items => select `Divvy` from `Applications`, once added click 'Hide'

### Vanilla

- open `Launch Vanilla.app`
- May need to adjust 'Allow apps downloaded from' setting in Security & Privacy in order to open
- Drag `Launch Vanilla.app` into `Applications`
- To start automatically on login: System Preferences => Users & Groups => Login Items => select `Launch Vanilla` from `Applications`, once added click 'Hide'

### Chrome Dev Tools

- Ensure [Material Theme Collection](https://chrome.google.com/webstore/detail/material-devtools-theme-c/jmefikbdhgocdjeejjnnepgnfkkbpgjo) is installed
- Go to chrome://flags
- Look for "Developer Tools experiments"
- Enable it and restart Chrome
- Open Developer Tools
- Settings > Experiments > "Allow Custom UI Themes"
- Settings > Preferences > Themes -> "Dark"
- Close and reopen DevTools

### Finder

### Terminal

* [Homebrew](https://brew.sh/)

#### Launch terminal hotkey

1. Install `Launch Terminal.workflow`
2. System Preferences => Keyboard => Shortcuts => Services - scroll down to General, then assign `Launch Terminal` to ⌘§

#### Smoother show/hide animation for Dock

```shell
remove_dock_animation_show_time.sh
```

### [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh)

#### [Spaceship](https://github.com/denysdovhan/spaceship-prompt) 🚀

```shell
git clone https://github.com/denysdovhan/spaceship-prompt.git "$ZSH_CUSTOM/themes/spaceship-prompt" --depth=1
ln -s "$ZSH_CUSTOM/themes/spaceship-prompt/spaceship.zsh-theme" "$ZSH_CUSTOM/themes/spaceship.zsh-theme" 
```

### [Powerline fonts](https://github.com/powerline/fonts) (required for Spaceship) ⚡️

```shell
git clone https://github.com/powerline/fonts.git --depth=1
cd fonts
./install.sh
cd ..
rm -rf fonts
```

#### [Zsh Notifier](https://github.com/marzocchi/zsh-notify) 🚨

```shell
brew install terminal-notifier
git clone git@github.com:marzocchi/zsh-notify.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/notifyln -s "$ZSH_CUSTOM/themes/spaceship-prompt/spaceship.zsh-theme" "$ZSH_CUSTOM/themes/spaceship.zsh-theme" 
```

#### [Autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) 💬

```shell
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

#### [Syntax Highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) 💅

```shell
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

#### [History Substring Search](https://github.com/zsh-users/zsh-history-substring-search) 🕰

```shell
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

### Developer

- Install Node
  
* Download XCode from [Mac App Store](https://apps.apple.com/gb/app/xcode/id497799835?mt=12)

### Github

#### SSH Keys

* [Add new key](https://github.com/settings/ssh/new)

```shell
ssh-keygen -t ed25519 -C "your_email@example.com"
# can leave passphrase empty
pbcopy < ~/.ssh/id_ed25519.pub
```

Paste copied key into Github

#### Slack

Copy custom Material Dark theme and paste into Slack:

```
#1A1A1A,#212121,#FF9800,#FFFFFF,#FF9800,#FFFFFF,#2EB67D,#FF9800,#1A1A1A,#727272
```
