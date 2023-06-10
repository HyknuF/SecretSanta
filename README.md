# Secret Santa Generator

Free (as in Freedom), simple and Open Source Secret Santa generator

## Background / Info

Last year, I couldn't find a tool with this feature set, therefore i wrote my own :)

- It randomly triggers Secret Santa groups based on their names and sends an email to all participants.
- The number of participants is dynamic and arbitrary.
- **Communication with the mail server is SSL encrypted.**
- It's a commandline tool, no fancy GUI and such. Only you and the text.
- Cross-Platform: Linux / Windows tested (with binaries), MacOS not tested but should run just fine.
- It creates a zip-file with single txt-files for each participant. This becomes handy if an email doesn't reach the participant for any reason.

## Advantages

- Even the planner does not know the Secret Santa groups. 
- E-mails are automatically generated with all key data and sent to all participants.
- No hassle for the planner

## Usage

If you have a working python environment installed, you can just use the "secretsanta_xx.py" in your preferred language and run it.

If not, no problem, it's simple: (German version only so far)
- Download the zip file from the latest release [HERE](https://codeberg.org/noxis/secret_santa_generator/releases)
- Unzip it and run the binary inside (i.e. secretsanta.exe)

## Build from Source

If you want to build your own binary from source, just download the secretsanta.py and install pyinstaller on your system (usually "**python -m pip install pyinstaller**").  
Afterwards run "**pyinstaller secretsanta.py**" and let the magic happen :)

## Todo

- Find a delightful name