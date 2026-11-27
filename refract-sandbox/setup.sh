#!/usr/bin/env bash
# Runs the Windows Refract build headless on Linux: extract app.asar, run with Linux Electron on Xvfb.
# Usage: setup.sh /path/to/Refract-*-win-x64.zip [workdir]
set -e
ZIP=$1; W=${2:-$HOME/refract-sb}; mkdir -p "$W"; cd "$W"
rm -rf x app && mkdir x && unzip -q "$ZIP" -d x
npx -y @electron/asar extract x/Refract/resources/app.asar app
V=$(strings x/Refract/Refract.exe | grep -m1 -oE 'Electron/[0-9.]+' | cut -d/ -f2)
mkdir -p el && cd el && [ -f package.json ] || npm init -y >/dev/null
npm i "electron@$V" >/dev/null && node node_modules/electron/install.js
echo "Ready: S=$W xvfb-run -a -s '-screen 0 1920x1080x24' node $(dirname "$0")/shot.js out.png"
