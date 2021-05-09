import ds3
import time
import mem


def reloadMap():
    print('Reloading map.')
    process = mem.getProcess()
    base_addr = mem.getBaseAddr(process.pid)
    last_bonfire = ds3.getLastBonfire(process, base_addr)
    print(
        f'Last Bonfire: {ds3.bonfires[str(last_bonfire)]} ({hex(last_bonfire)})')
    coords = ds3.getPlayerCoords(process, base_addr)
    angle = ds3.getPlayerAngle(process, base_addr)
    ds3.warpToBonfire(process, base_addr, last_bonfire)
    ds3.writePlayerPosition(process, base_addr, coords, angle)
