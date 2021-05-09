# Dark Souls III Hot Reloading [WIP]

This project aims to solve a minor inconvenience in DS3 modding by replacing manual reloading with auto reloading.

Video demo:

https://www.youtube.com/watch?v=Ysozp4yajrw

This is still a work in progress. It does not cover a big amount of edge-cases. Feel free to test it and contribute.

Tested on: Windows 10 x64, Dark Souls III v1.15 (no DLCs)

# Required libraries:

- ctypes
- pypiwin32
- ReadWriteMemory
- watchdog

# Usage

0. Modify the mod folder path in config.json
1. Open DS3 and load your latest save
2. Navigate to the desired area you are editing right now
3. Use the nearest bonfire
4. Go to the position you wish to be telepored after area reload
5. If you are using Debug Menu, enable the sliders you need
6. Launch main.exe
7. Edit some files in your mod folder, the area should reload and preserve your character coords and angle accordingly