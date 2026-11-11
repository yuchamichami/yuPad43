"""Decode IQS9151 bytes read from 0x1014 (28 bytes). No I2C or HID transport."""
def decode_frame(data):
    if len(data) != 28:
        raise ValueError('Expected 28 bytes starting at 0x1014')
    def u16(o): return int.from_bytes(data[o:o+2], 'little')
    def s16(o): return int.from_bytes(data[o:o+2], 'little', signed=True)
    info, flags = u16(12), u16(14)
    return {'dx': s16(0), 'dy': s16(2), 'single_gestures': u16(8),
            'two_finger_gestures': u16(10), 'info_flags': info,
            'trackpad_flags': flags, 'finger_count': flags & 15,
            'ati_error': bool(info & 8), 'show_reset': bool(info & 128),
            'finger1_confident': bool(flags & 256),
            'finger1_x': u16(16), 'finger1_y': u16(18),
            'finger1_strength': u16(20), 'finger1_area': u16(22),
            'finger2_x': u16(24), 'finger2_y': u16(26)}
