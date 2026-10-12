# PNG Forensics Challenge – Find the Flag

**Goal:** find the hidden flag (format `flag{...}`) in `challenge.png`.

**Flag:** `flag{g0t_1t_in_pLAin_sight}`

## Files
- `challenge.png` – the original (corrupted) challenge file
- `challenge_fixed.png` – the repaired image, flag visible at the bottom
- `solve.py` – script that repairs the file automatically

## Approach (short)
1. The file would not open, so I inspected its raw bytes and PNG chunks.
2. The IHDR header said the height was 800, but its CRC checksum only matched a height of 850. The bottom 50 rows (with the flag) were hidden.
3. A fake `IEND` chunk (12 bytes) was inserted at offset `0x21C89` inside the image data, corrupting everything after it.
4. I removed the fake chunk and restored the true height. The CRC checks then matched and the image decoded cleanly.

## Tools
Python 3 (`struct`, `zlib`, Pillow), HxD hex editor.

## How to run
```
pip install pillow
python solve.py
```
This creates `challenge_fixed.png`.
