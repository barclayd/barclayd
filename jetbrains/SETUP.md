# Webstorm Setup

After downloading Webstorm, to get it configured with the familiar plugins, keybindings and config do the following:

* File -> Manage IDE Settings -> Import Settings -> ~/<PATH_TO_THIS_REPO>/webstorm/Settings.zip

* DO NOT SETUP ACCOUNT SETTING SYNC WITH WEBSTORM - this will cause headaches and will damage setup on other devices using Webstorm with the same license and has yet to be proven as successful

## UI Tweaks

* Enable `MaterialTheme` > `High Contrast` and `Constrast Mode`

### Setting up correct UI Font

<p align="center">
<img width="100%" alt="image" src="https://github.com/user-attachments/assets/4e3786b9-2817-4cfa-821e-6ade74230f2a">
<img width="100%" alt="image" src="https://github.com/user-attachments/assets/d917edd2-d569-4544-929a-f681f8c39968">
</p>

### WebStorm Configuration

#### Prettier
- Preferences => External Tools
- Import [Prettier tool](https://github.com/barclayd/barclayd/tree/master/webstorm/Prettier.xml)
- Setup key mapping
- Preferences => Prettier => Enable 'on code reformat' and 'on save'