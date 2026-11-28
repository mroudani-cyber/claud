# Refract sandbox (editing side)
Runs the Windows Refract build (tested 0.3.7, Electron 45.5.0) inside a Linux cloud session:
`setup.sh <zip>` extracts `app.asar` and installs the matching Linux Electron; `shot.js` launches it on Xvfb.
Note: the app's ffmpeg lookup is Windows-oriented; the system `/usr/bin/ffmpeg` is used where possible.
