"""Repair a tampered PNG (CTF challenge) and reveal the hidden flag.

Two things were wrong with the file:
  1. The height in the IHDR header was changed (850 -> 800), hiding the bottom rows.
  2. A fake 12-byte IEND chunk was planted inside the image data, corrupting it.
"""
import struct
import zlib

SRC = "challenge.png"
OUT = "challenge_fixed.png"

data = bytearray(open(SRC, "rb").read())

# --- Step 1: remove the fake IEND chunk (length 0 + 'IEND' + CRC = 12 bytes) ---
fake = bytes.fromhex("00000000" "49454e44" "ae426082")
first = bytes(data).find(fake)
last = bytes(data).rfind(fake)
if first != -1 and first != last:          # an extra IEND before the real final one
    print(f"Fake IEND found at offset {first} (hex {first:X}), removing 12 bytes")
    del data[first:first + 12]
else:
    print("No fake IEND found")

# --- Step 2: recover the true image height from the IHDR checksum ---
width = struct.unpack(">I", data[16:20])[0]
tail = bytes(data[24:29])                   # bit depth, colour type, etc.
stored_crc = struct.unpack(">I", data[29:33])[0]
for h in range(1, 10000):
    if zlib.crc32(b"IHDR" + struct.pack(">II", width, h) + tail) == stored_crc:
        print(f"True height is {h} (header said {struct.unpack('>I', data[20:24])[0]})")
        data[20:24] = struct.pack(">I", h)
        break

open(OUT, "wb").write(data)
print("Saved", OUT)
