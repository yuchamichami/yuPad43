# Integration with other firmware

[日本語](integration.md) | English

For RMK, QMK, or custom firmware, provide I²C communication, GPIO handling, timing, and host mouse/scroll output. yuPad43 communicates over I²C; the host generates USB or Bluetooth input reports.

Use [yuPad43-profile.json](../data/yuPad43-profile.json) for initialization blocks, RX/TX mapping, and configuration overrides. [register-writes.csv](../data/register-writes.csv) lists the base register writes. Apply the overrides and startup sequence below in addition to the CSV data.

## Configuration

| Item | Value |
| --- | --- |
| I²C address | 0x56, 7-bit |
| Product ID | Read 0x1000 and check for 0x09BC |
| I²C speed | 100 kHz |
| Register addresses and 16-bit values | Little-endian |
| RX / TX | 10 / 9; use the mapping in the JSON |
| Coordinate resolution | X=1300, Y=1192; these are coordinate settings, not DPI or measured edge coverage |
| ATI target | 400 |
| Touch thresholds | Touch: 30; release: 26 |
| Finger Split Factor | 0; splitting of adjacent touch regions is disabled |
| ALP / SW_IN | Disabled; TX45 is used as an electrode |

## Communication

Access the IC during a communication window when RDY is physically low. To read, send the two-byte register address, issue a repeated START, read the data, and finish with STOP. For example, the address bytes for 0x1014 are `14 10`. Account for whether your GPIO API returns the physical pin level or an active-low logical state.

The configuration closes the communication window on STOP. Wait for a new window before accessing another register, including when splitting configuration writes. The ZMK driver writes at most 30 bytes per transaction. Discard failed or timed-out reads rather than interpreting them as valid frames.

## Startup sequence

1. Check power and RDY, then read the product ID.
2. Reset the IC, check Show Reset, and acknowledge it using Ack Reset (System Control bit 7).
3. Write the JSON's `base_write_blocks` in order, followed by `post_write_overrides`. Apply the rotation override as a read-modify-write operation, preserving the other bits.
4. Request TP Re-ATI using bit 5 of register 0x11BC. Starting from zero, the data bytes are `20 00`; preserve other bits when modifying an existing control value.
5. Wait for communication to resume, then check RDY and ATI completion within a bounded timeout. Read ATI error separately from Info Flags bit 3.
6. Read normal frames and convert finger detection and movement into host input events.

ATI completion and the ATI quality flag are separate. The quality flag indicates compensation reaching its limits or counts outside the recalibration range immediately after calibration. It does not identify a disconnected pin. The user driver continues processing valid input when this flag is set. Keep communication failures, configuration write failures, and incomplete calibration separate from this advisory flag. Handle Show Reset during operation with the appropriate host-side recovery and configuration sequence.

For scroll-only behavior, accumulate movement into wheel output and retain fractional remainders rather than discarding small movements through integer rounding. Tap actions and two-finger gesture assignments are handled by the host firmware.

## Output data

The driver reads 28 bytes starting at 0x1014. [decode_frame.py](../data/decode_frame.py) demonstrates how to interpret an already-read frame; it does not perform I²C communication or generate mouse output.

| Address | Format | Contents |
| --- | --- | --- |
| 0x1014 / 0x1016 | int16 / int16 | Relative X / Y movement |
| 0x101C / 0x101E | uint16 / uint16 | One-finger / two-finger gesture flags |
| 0x1020 | uint16 | Info Flags: bit 3 ATI error, bit 7 Show Reset |
| 0x1022 | uint16 | Trackpad Flags: bits 0–3 finger count, bits 8/9 confidence for fingers 1/2 |
| 0x1024 / 0x1026 | uint16 / uint16 | Finger 1 X / Y |
| 0x1028 / 0x102A | uint16 / uint16 | Finger 1 signal strength / area |
| 0x102C / 0x102E | uint16 / uint16 | Finger 2 X / Y |

Use finger count and confidence together; coordinates in a release frame do not represent a new touch. Decode relative movement as signed values. Signal strength is not a force measurement in newtons. Swap or invert axes to match the mounting orientation, then verify by moving a finger rightward and downward.

Normal cursor and scroll operation does not require electrode-level readings. Inspection tools can read the 10 × 9 Count, Reference, and Delta matrices from separate registers. Keep intensive matrix sampling separate from normal operation to avoid adding input latency.

See the communication, ATI, and register sections of the [Azoteq IQS9150/IQS9151 datasheet, v1.2](https://www.azoteq.com/images/stories/pdf/IQS9150_IQS9151_datasheet.pdf).

[Back to the connection and usage guide](../README.en.md)
