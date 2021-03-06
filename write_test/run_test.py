import subprocess
import os, sys
import struct
path = '../../s3g/'
sys.path.insert(0, path)

import makerbot_driver

port = '/dev/tty.usbmodemfa131'

s3g = makerbot_driver.s3g.from_filename(port)

num_cycles = 10000
eeprom_length = 4000

name = 'write_test_eeprom.hex'

for i in range(num_cycles):
    print "Writing eeprom values"
    for j in range(0, eeprom_length, 10):
        if j == 330:
            pass
        else:
            val = j % 256
            packed_val = struct.pack('<B', val)
            s3g.write_to_EEPROM(j, packed_val)

    print "Pulling the hex file"
    subprocess.check_call(['avrdude', '-cstk500v1', '-pm1280', '-P%s' % (port), '-b57600', '-Ueeprom:r:%s:i' % (name)])

    print "Adding File to repo"
    subprocess.check_call(['git', 'add', name])

    print "Committing File to repo"
    try:
        subprocess.check_call(['git', 'commit', '-m', 'Running Write Test.  Iteration: %i' % (i)])
    except subprocess.CalledProcessError as e:
        print "Nothing to commit, yay!"
