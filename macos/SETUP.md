# Documented Steps for an Opinionated MacBook Configuration

```shell
git clone https://github.com/barclayd/barclayd
```

### Setup tracking for `.zshrc` and `Brewfile` via Symlink

Run the following command from the root directory to automatically track changes to `.zshrc`

```shell
ln -s ~/<PATH_TO_THIS_REPO>/.zshrc ~/.zshrc
ln -s ~/<PATH_TO_THIS_REPO>/.spaceshiprc.zsh ~/.spaceshiprc.zsh
ln -s ~/<PATH_TO_THIS_REPO>/macos/Brewfile ~/Brewfile
```

### Setup tracking for `.gitignore` via Symlink to global `.gitignore`

```shell
ln -s ~/<PATH_TO_THIS_REPO>/.gitignore ~/.gitignore_global
git config --global core.excludesfile ~/.gitignore_global
git config --global user.email daniel.barclay@lloydsbanking.com
git config --global --add --bool push.autoSetupRemote true
```

This will create a symlinked version of the tracked `.zshrc` and `.gitignore` available in your root directory

### System Preferences

- Mission Control => Hot corners - bottom right = 'Put Display to Sleep'
- Siri => Enable Siri
- Desktop & Screen Saver => start after: Never
- Sharing => Rename Computer Name
- General => Appearance Auto

### Mac Apps

### CopyClip

- [CopyClip (direct)](https://fiplab.com/app-download/CopyClip_2.zip)

- [CopyClip (Mac app store)](https://apps.apple.com/us/app/copyclip-clipboard-history/id595191960?mt=12)

Configure to show menu using <kbd>Cmd</kbd> + <kbd>option</kbd> + <kbd>space</kbd>

#### [Divvy (deprecated)](https://apps.apple.com/gb/app/divvy-window-manager/id413857545?mt=12)

Setup global shortcuts

<p align="center">
<img width="300px" alt="Screenshot 2021-01-24 at 11 58 17" src="https://user-images.githubusercontent.com/39765499/105629561-9d4bbd00-5e3b-11eb-9a6d-4438be7501d8.png">
</p>

<p align="center">
<img width="300px" alt="Screenshot 2021-01-24 at 11 57 54" src="https://user-images.githubusercontent.com/39765499/105629564-a0df4400-5e3b-11eb-913f-705e5fabeb4e.png">
</p>

- To start automatically on login: System Preferences => Users & Groups => Login Items => select `Divvy` from `Applications`, once added click 'Hide'

#### [Magnet](https://apps.apple.com/gb/app/magnet/id441258766?mt=12)

Setup global shortcuts

<p align="center">
<img width="100%" alt="image" src="https://user-images.githubusercontent.com/39765499/212909228-df0a6a04-5b4f-4bbf-848d-30fbe0c9858c.png">
</p>

- To start automatically on login: System Preferences => Users & Groups => Login Items => select `Divvy` from `Applications`, once added click 'Hide'

## Chrome Extensions

## Refined Github

* [1password](https://chrome.google.com/webstore/detail/1password-%E2%80%93-password-mana/aeblfdkhhhdcdjpifhhbdiojplfjncoa)
* [Refined Github](https://chrome.google.com/webstore/detail/refined-github/hlepfoohegkhhmjieoechaddaejaokhf)
* [React Developer Tools](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
* [Atom Material Icons](https://chrome.google.com/webstore/detail/atom-material-icons/pljfkbaipkidhmaljaaakibigbcmmpnc)

### Chrome Dev Tools

- Ensure [Material Theme Collection](https://chrome.google.com/webstore/detail/material-devtools-theme-c/jmefikbdhgocdjeejjnnepgnfkkbpgjo) is installed
- Open Developer Tools
- Open the Settings:
  - > Preferences -> Theme -> Dark
  - > Experiments > "Allow extensions to load custom stylesheets"
  - > Devices > `Nexus 5`, `Nexus 5X`, `Pixel 4`, `iPhone 6/7/8 Plus`
- Close and reopen the DevTools

### Finder

- Open Finder, right click to select 'Customise Toolbar'
- Open a new Finder windows => navigate to 'Applications'
- Drag apps that you wish to open code up in (e.g. Webstorm, VSCode, XCode, terminal)
- Enable "Show Path Bar"

<p align="center">
<img width="300px" alt="Screenshot 2021-01-24 at 11 57 54" src="https://user-images.githubusercontent.com/39765499/105882836-0b3fe200-5ffe-11eb-937c-7c03b3da6813.png">
</p>

### Terminal

##### Theme

Terminal -> Preferences -> Import -> ~/<PATH_TO_THIS_REPO>/macos/Terminal Theme/MaterialDarker.terminal

- [Homebrew](https://brew.sh/)

Setups to install Homebrew, preconfigured with basic packages:

Ensure a git email address has been setup globally before starting these steps

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew bundle --file ~/Brewfile
```

#### Launch terminal hotkey

1. Install `Launch Terminal.workflow`
2. System Preferences => Keyboard => Shortcuts => Services - scroll down to General, then assign `Launch Terminal` to ⌘§

#### Smoother show/hide animation for Dock

```shell
remove_dock_animation_show_time.sh
```

### [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh)

##### Installation

```shell
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

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
..
rm -rf fonts
```

Then in the Terminal, configure the font to be the following:

<p align="center">
<img width="75%" alt="Screenshot 2023-01-20 at 12 14 04" src="https://user-images.githubusercontent.com/39765499/213692634-824ed028-3179-4975-b28a-610fb2d9706e.png">
</p>


#### [Zsh Notifier](https://github.com/marzocchi/zsh-notify) 🚨

```shell
git clone https://github.com/marzocchi/zsh-notify.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/notify
```

#### [Autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) 💬

```shell
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

#### [Syntax Highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) 💅

```shell
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

#### [History Substring Search](https://github.com/zsh-users/zsh-history-substring-search) 🕰

Installed via Brewfile

If not working after installation - check contents of `.zshrc` and re-do symlink if necessary

### Developer


#### Node

- Install via NVM [NVM](https://github.com/nvm-sh/nvm)

```shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
```

Restart terminal after completing command and verify installation by running:

```shell
nvm -v
```

- Install Node 16 via NVM as default

```shell
nvm install 16 --default
```

### Rust

```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

* `enter 1 when prompted`

- Download XCode from [Mac App Store](https://apps.apple.com/gb/app/xcode/id497799835?mt=12)
- Download [Postman](https://www.postman.com/downloads/)

### Github

#### SSH Keys

- [Add new key](https://github.com/settings/ssh/new)

```shell
ssh-keygen -t ed25519 -C "barclaysd@me.com"
# can leave passphrase empty
pbcopy < ~/.ssh/id_ed25519.pub
```

Paste copied key into Github

##### If facing issues with git cloning a repository do the following:

Issue:

```shell
The authenticity of host 'github.com' can't be established.
ECDSA key fingerprint is SHA256:Gqa14BKiB8EhFtUBGrtb4LA2M2Y6D6rpJTMXq7oplD8.
This key is not known by any other names
```

Fix:

```shell
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

Note that the host name can be swapped out in both commands depending on the base domain of the repo you are cloning

#### Setting up dual ssh keys

Reference individual `git.conf` files to house access to multiple [github.com](github.com) accounts from the same computer.

Add the following to `~/.gitconfig`:

```
[include]
	path = ~/work.conf
[includeIf "gitdir:~/Documents/Coding/"]
	path = ~/personal.conf
```

Add the following `work.conf` file to `~`:

```
[user]
	email = <work email>
	name = Daniel Barclay
```

Add the following `personal.conf` file to `~`:

```
[user]
	email = barclaysd@me.com
	name = Daniel Barclay

[github]
	user = "barclayd"

[core]
	sshCommand = "ssh -i ~/.ssh/personal_github"
```

### .npmrc 

Improve `npm i` times by running the following:

```shell
echo "audit=false" >> ~/.npmrc
```

#### Slack

Copy custom Material Dark theme and paste into Slack:

```
#1A1A1A,#212121,#FF9800,#FFFFFF,#FF9800,#FFFFFF,#2EB67D,#FF9800,#1A1A1A,#727272
```

### Docker

- Download and install [Docker for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac/)

### Webstorm

#### Prettier

- Open Webstorm, go to Preferences => External Tools
- Copy the [Prettier tool](https://github.com/barclayd/barclayd/tree/master/webstorm/Prettier.xml) xml file into webstorm as a new external tool
- Ensure key mapping is setup
- Ensure no projects are open, go to Preferences => Prettier and ensure both 'on code reformat' and 'on save' options are checked. Click 'Apply'

#### ESLint

- Ensure no projects are open, go to Preferences => ESLint and ensure 'automatic ESLint configuration' is selected. Click 'Apply'

### Swift Development

- [Swift Format](https://github.com/nicklockwood/SwiftFormat)
- [XCode duplicate line keymapping](https://gist.github.com/emotality/b1bcb2bb8a07921f9c8cad1c969daedf)

### Custom app keyboard shortcuts

* Follow the screenshot below to add custom app keyboard shortcuts that are missing to installed Mac applications
* Ensure menu option names match exactly:
    - Menu Title: `Duplicate tab`
* Assign to <kbd>control</kbd> + <kbd>⇧</kbd> + <kbd>D</kbd>

<p align="center">
<img width="500" alt="mac keyboard shortcuts" src="https://user-images.githubusercontent.com/39765499/112757733-f32b1580-8fe2-11eb-9483-136a37f6461f.png">
</p>

### Other

- If items saved to Desktop are not displaying run `show_desktop_icons.sh`

### Cursor

* Change `workbench.activityBar.orientation` to `vertical`
* Move activity bar to the right
* Install the following extensions:
	* Material Icon Theme
	* Material Theme - Free - Select Material Darker High Contrast
  	* Open in Github

### Mac Apps

* ChatGPT
* 1Password
* Magent
* HiddenBar
* CopyClip 2
