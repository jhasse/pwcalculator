# Password Calculator [![Build Status](https://travis-ci.org/jhasse/pwcalculator.svg?branch=v1.1)](https://travis-ci.org/jhasse/pwcalculator)

This app calculates strong passwords for each alias from your single secret. No need to remember
dozens of passwords any longer and no need for a password manager! Based on this GNOME Shell
extension: https://extensions.gnome.org/extension/825/password-calculator/

Icon made by [Madebyoliver](http://www.flaticon.com/authors/madebyoliver) from
[www.flaticon.com](http://www.flaticon.com) is licensed by
[CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/).

## Dependencies

### Ubuntu Linux

```sh
sudo apt install libssl-dev libwxgtk3.0-dev libboost-dev
```

### Fedora Linux

```sh
sudo dnf install gcc-c++ wxGTK3-devel openssl-devel boost-devel
```

### Windows (MSYS2)

```sh
pacman -S mingw-w64-x86_64-wxWidgets mingw-w64-x86_64-waf
```

## Build and Run

```sh
./waf configure build # Linux
waf configure build # Windows (MSYS2)
./build/pwcalculator
```

## Install (Linux only)

```sh
./waf configure build --release
sudo ./waf install
sudo chmod +x /usr/local/share/applications/com.bixense.PasswordCalculator.desktop
```

## Creating a Flatpak

```sh
flatpak install gnome org.gnome.Sdk 3.22
flatpak install gnome org.gnome.Platform 3.22
flatpak-builder --repo=repo ./build com.bixense.PasswordCalculator.json
flatpak build-bundle repo pwcalculator.flatpak com.bixense.PasswordCalculator
```
