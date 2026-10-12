# BYTE PNG challenge
**Task:** Find the hidden flag (format `flag{...}`) in a corrupted PNG file.

**Flag:** `flag{g0t_1t_in_pLAin_sight}`

## Files
- `challenge.png` - original corrupted file
- `challenge_fixed.png` - repaired image (flag visible at the bottom)
- `screenshots` - my HxD steps

## Tools
- HxD hex editor

## How I did it
1. I downloaded the corrupted PNG. It would not open normally.
2. I opened it in HxD and searched for `flag{` thinking that the flag would be in chunks but found nothing, because
   the flag is part of the image pixels.
3. I learned that a PNG is made of chunks, and each chunk has a CRC
   checksum that detects tampering.
4. I found two problems:
   - The height in the header was changed from 850 to 800, which hid the
     bottom 50 rows where the flag was. Only 850 matched the header's CRC.
   - A fake `IEND` chunk (12 bytes) was placed inside the image data at
     offset `0x21C89`. A valid PNG has `IEND` only once, at the end.
5. I fixed it in HxD: changed the height bytes from `00 00 03 20` to
   `00 00 03 52`, and deleted the 12 fake bytes
   `00 00 00 00 49 45 4E 44 AE 42 60 82`.
6. I saved the file and opened it. The flag was in the bottom strip.

## What I learned
- PNG files are built from chunks (IHDR, IDAT, IEND), each with a CRC.
- Checksums reveal tampering and confirm that a fix is correct.
- A changed header height can hide part of an image.
