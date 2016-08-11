# -*- coding: utf-8 -*-

import smbus


class GP2Y0E02B(object):

    # take the left 7 bits of the default address byte
    # (the lsb of the byte is then set to either 0 or 1 depending on
    # read/write operations)
    DEFAULT_DEVICE_ADDR = 0x80 >> 1

    # Shift bit at 0x35:
    # 0x01=Maximum Display 128cm
    # 0x02=Maximum Display 64cm
    SHIFT_BIT_ADDR = 0x35

    # 0x5E is Distance[11:4]
    # 0x5F is Distance[3:0]
    # Distance Value = (Distance[11:4]*16+Distance[3:0])/16/2^n
    # n : Shift Bit (Register 0x35)
    DISTANCE_ADDR = 0x5E

    # 0xE8: Active/Stand-by State Control
    STATE_CONTROL_ADDR = 0xE8
    STATE_ACTIVE = 0x00
    STATE_STANDBY = 0x01

    def __init__(self, bus=1, addr=DEFAULT_DEVICE_ADDR):
        self._i2c = smbus.SMBus(bus)
        self._addr = addr
        self._shift_bit = self._i2c.read_byte_data(addr, self.SHIFT_BIT_ADDR)

    @property
    def value(self):
        """Reads and returns the measured distance (unit: cm)"""
        # read the two distance bytes and return the distance in cm
        b1, b2 = self._i2c.read_i2c_block_data(self._addr,
                                               self.DISTANCE_ADDR, 2)
        return (b1 * 16 + b2) / 16 / (2 ** self._shift_bit)

    def stand_by(self):
        """
        Put the device in stand-by state
        (in this state it consumes only ~60uA instead of ~25mA)
        """
        self._i2c.write_byte_data(self._addr,
                                  self.STATE_CONTROL_ADDR, self.STANDBY_STATE)

    def wake_up(self):
        """
        Put the device in active state
        """
        self._i2c.write_byte_data(self._addr,
                                  self.STATE_CONTROL_ADDR, self.ACTIVE_STATE)
