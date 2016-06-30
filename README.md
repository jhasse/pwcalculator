# Password Calculator

This app calculates strong passwords for each alias from your single secret. No need to remember
dozens of passwords any longer and no need for a password manager! Based on this GNOME Shell
extension: https://extensions.gnome.org/extension/825/password-calculator/

Icon made by [Madebyoliver](http://www.flaticon.com/authors/madebyoliver) from
[www.flaticon.com](http://www.flaticon.com) is licensed by
[CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/).

## Dependencies

### Fedora Linux

```sh
sudo dnf install gcc-c++ wxGTK3-devel openssl-devel boost-devel
```

Workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1128365:

```sh
sudo ln -s /usr/bin/wx-config-3.0 /usr/local/bin/wx-config
```

## Build and Run

```sh
./waf configure build
./build/pwcalculator
```

## Install (Linux)

```sh
sudo ./waf install
```
