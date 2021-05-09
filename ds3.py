import mem
import time
import ctypes


bonfires = {
    '999': 'Shadow Realm',
    '4002950': 'Firelink Shrine',
    '4002959': 'Ashen Grave',
    '4002951': 'Cemetery of Ash',
    '4002952': 'Iudex Gundyr',
    '4002953': 'Untended Graves',
    '4002954': 'Champion Gundyr',
    '3002950': 'High Wall of Lothric',
    '3002955': 'Tower on the Wall',
    '3002952': 'Vordt of the Boreal Valley',
    '3002954': 'Dancer of the Boreal Valley',
    '3002951': 'Oceiros, the Consumed King',
    '3002960': 'High Wall of Lothric, Teleport',
    '3102954': 'Foot of the High Wall',
    '3102950': 'Undead Settlement',
    '3102952': 'Cliff Underside',
    '3102953': 'Dilapidated Bridge',
    '3102951': 'Pit of Hollows',
    '3302956': 'Road of Sacrifices',
    '3302950': 'Halfway Fortress',
    '3302957': 'Crucifixion Woods',
    '3302952': 'Crystal Sage',
    '3302953': 'Farron Keep',
    '3302954': 'Keep Ruins',
    '3302958': 'Farron Keep Perimeter',
    '3302955': 'Old Wolf of Farron',
    '3302951': 'Abyss Watchers',
    '3502953': 'Cathedral of the Deep',
    '3502950': 'Cleansing Chapel',
    '3502951': 'Deacons of the Deep',
    '3502952': 'Rosaria\'s Bed Chamber',
    '3802956': 'Catacombs of Carthus',
    '3802950': 'High Lord Wolnir',
    '3802951': 'Abandoned Tomb',
    '3802952': 'Old King\'s Antechamber',
    '3802953': 'Demon Ruins',
    '3802954': 'Old Demon King',
    '3702957': 'Irithyll of the Boreal valley',
    '3702954': 'Central Irithyll',
    '3702950': 'Church of Yorshka',
    '3702955': 'Distant Manor',
    '3702951': 'Pontiff Sulyvahn',
    '3702956': 'Water Reserve',
    '3702953': 'Anor Londo',
    '3702958': 'Prison Tower',
    '3702952': 'Aldrich, Devourer of Gods',
    '3902950': 'Irithyll Dungeon',
    '3902952': 'Profaned Capital',
    '3902951': 'Yhorm The Giant',
    '3012950': 'Lothric Castle',
    '3012952': 'Dragon Barracks',
    '3012951': 'Dragonslayer Armour',
    '3412951': 'Grand Archives',
    '3412950': 'Twin Princes',
    '3202950': 'Archdragon Peak',
    '3202953': 'Dragon-Kin Mausoleum',
    '3202952': 'Great Belfry',
    '3202951': 'Nameless King',
    '4102950': 'Flameless Shrine',
    '4102951': 'Klin of the First Flame',
    '4102952': 'The First Flame',
    '4502951': 'Snowfield',
    '4502952': 'Rope Bridge Cave',
    '4502953': 'Corvian Settlement',
    '4502954': 'Snowy Mountain Pass',
    '4502955': 'Ariandel Chapel',
    '4502950': 'Sister Friede',
    '4502957': 'Depths of the Painting',
    '4502956': 'Champion\'s Gravetender',
    '5002951': 'The Dreg Heap                        ',
    '5002952': 'Earthen Peak Ruins',
    '5002953': 'Within the Earthen Peak Ruins',
    '5002950': 'The Demon Prince',
    '5102110': 'The Ringed City',
    '5102952': 'Mausoleum Lookout',
    '5102953': 'Ringed Inner Wall',
    '5102954': 'Ringed City Streets',
    '5102955': 'Shared Grave',
    '5102950': 'Church of Filianore',
    '5112951': 'Filianore\'s rest',
    '5112950': 'Slave Knight Gael',
    '5102951': 'Darkeater Midir',
    '4602950': 'Grand Rooftop',
    '4702950': 'Kiln of Flame',
    '5302950': 'Dragon Ruins',
    '5402950': 'Round Plaza'}


BaseAOffset = 0x4740178
BaseBOffset = 0x4768E78
BaseCOffset = 0x4743AB0


def getLastBonfire(process, base_addr):
    return mem.readWithOffsets(process, base_addr + BaseCOffset, [0xACC])


def createWarpByteCode(bonfire, base_addr, thread_addr):
    offset_1 = (base_addr + 0x473A9C8) - thread_addr - 0x7 - 0x4
    print(f'Offset 1: {hex(offset_1)}')
    offset_1 = offset_1.to_bytes(4, byteorder='little')
    offset_2 = 0x140475DC0 - thread_addr - 0x24 - 0x5
    print(f'Offset 2: {hex(offset_2)}')
    offset_2 = offset_2.to_bytes(4, byteorder='little')
    return ctypes.create_string_buffer(bonfire.to_bytes(4, byteorder='little') +
                                       b'\x48\x8B\x0D'
                                       + offset_1
                                       + b'\x4C\x8B\x05\xEE\xFF\xFF\xFF\x41\x8D\x90\x18\xFC\xFF\xFF\x45\x8D\x80\x18\xFC\xFF\xFF\x48\x83\xEC\x28\xE8'
                                       + offset_2
                                       + b'\x48\x83\xC4\x28\xC3')


def getPlayerCoords(process, base_addr):
    preWarpCoords_x = mem.readWithOffsets(
        process, base_addr + BaseBOffset, [0x40, 0x28, 0x80])
    preWarpCoords_y = mem.readWithOffsets(
        process, base_addr + BaseBOffset, [0x40, 0x28, 0x88])
    preWarpCoords_z = mem.readWithOffsets(
        process, base_addr + BaseBOffset, [0x40, 0x28, 0x84])
    return ctypes.create_string_buffer(
        preWarpCoords_x.to_bytes(4, byteorder='little')
        + preWarpCoords_z.to_bytes(4, byteorder='little')
        + preWarpCoords_y.to_bytes(4, byteorder='little')
    )


def getPlayerAngle(process, base_addr):
    preWarpCoords_angle = mem.readWithOffsets(
        process, base_addr + BaseBOffset, [0x40, 0x28, 0x74])
    return ctypes.create_string_buffer(
        preWarpCoords_angle.to_bytes(4, byteorder='little')
    )


def writePlayerPosition(process, base_addr, coords, angle):
    mem.writeWithOffsets(process,  base_addr +
                         BaseBOffset, [0x40, 0x28, 0x80], coords)

    mem.writeWithOffsets(process,  base_addr +
                         BaseBOffset, [0x40, 0x28, 0x74], angle)


def waitForWarp(process, base_addr):
    coords = 0x0
    while coords == 0x0:
        coords = mem.readWithOffsets(process, base_addr +
                                     BaseBOffset, [0x40, 0x28, 0x74])


def freeWarpMemory(process, addr):
    mem.free(process, addr)


def warpToBonfire(process, base_addr, bonfire):
    LEN_WARP_BYTECODE = 47
    thread_addr = mem.alloc(process, 0x13FF00000, 47)
    try:
        warp_bytecode = createWarpByteCode(bonfire, base_addr, thread_addr)
        mem.writeMem(process, thread_addr, warp_bytecode)
        thread_start_addr = thread_addr + 0x4
        print(hex(thread_start_addr))
        mem.createThreadSimple(process, thread_start_addr)
        time.sleep(10)
        waitForWarp(process, base_addr)
        time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        freeWarpMemory(process, thread_addr)
