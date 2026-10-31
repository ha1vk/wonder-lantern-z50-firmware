# Wonder Lantern Z50

**English** | [简体中文](README.md)

Custom shutter-sound patch firmware for the **Nikon Z50 (first generation)** running firmware **C 2.60** (main module `eg1630_026000.bi`).

> ⚠️ **Only for the Nikon Z50 (first generation) + C 2.60 firmware**. Flashing onto other models (Z30/Zfc/Z6/Z7/Z8/Z9, Z50 II) or other firmware versions may brick the camera immediately.
> Stock checksum: `eg1630_026000.bi` SHA-256 `57e834fac8f921c18c99abe0b1469edbaca71cb1957794bb9f138bd223d30fc1`, size 31,404,090 bytes.

## Porting status
- Contains only the **shutter-sound (custom electronic shutter sound)** feature
- Custom menu now has Chinese labels
- Added function to view shutter count information

## Features

- A **Shutter sound** entry appears in the setup menu (last row of the wrench SETUP menu):

  ```text
  Enabled          OFF / ON
  Sound file       None / SHUTTER.WAV / 1.WAV..4.WAV
  Preview sound    (preview; works even when OFF)
  Reload sound     (reload the current file from the SD card)
  ```

- UI follows the camera body language (Simplified Chinese / Traditional Chinese / English)
- Config is saved to `WL-SOUND.CFG` in the SD card root; restored automatically the first time the menu is opened or the first shot after reboot

## Trigger conditions (important)

The custom sound **only fires when all of the following are true**:

1. This feature is `Enabled = ON` (and a valid sound file is selected)
2. **Silent photography = ON** on the camera
3. An actual shot is taken (half-press / video recording etc. will not trigger it)

**Pressing the shutter without silent photography = stock shutter sound, the custom sound does not play.** This is intentional: in silent mode the stock sound is suppressed and replaced by the custom sound; in non-silent mode the stock sound is kept.

## Audio format and preparation

SD card layout (fixed file names, case-insensitive):

```text
SD card root
├── SHUTTER.WAV          (Sound file item 1: SHUTTER.WAV)
└── SHUTTER/             (folder)
    ├── 1.WAV            (Sound file item 2: 1.WAV)
    ├── 2.WAV            (Sound file item 3: 2.WAV)
    ├── 3.WAV            (Sound file item 4: 3.WAV)
    └── 4.WAV            (Sound file item 5: 4.WAV)
```

Besides `SHUTTER.WAV` in the root, the `SHUTTER` folder may contain up to 4 files, `1.WAV`, `2.WAV`, `3.WAV`, `4.WAV`, selectable via `Sound file` in the menu. Format requirements for each file:

- Standard 44-byte WAV header (no extra chunks)
- Uncompressed PCM (format=1), **mono**, **8000 Hz**, **16-bit signed little-endian**
- Non-empty, max **1.08 seconds** (data ≤ 17280 bytes)

Normalize any WAV with `prepare_wav.py` first:

```sh
python3 prepare_wav.py your_sound.wav SHUTTER.WAV
python3 prepare_wav.py your_sound.wav 1.WAV
```

The script converts to mono, resamples to 8 kHz and truncates to 1.08 seconds. Input must be 8/16/24/32-bit integer PCM.

## Usage

1. Prepare `SHUTTER.WAV` and place it in the **SD card root**
2. Insert the card and power on → menu → SETUP menu → Shutter sound
3. `Sound file` → select `SHUTTER.WAV` (selecting does not enable or play the sound automatically)
4. `Enabled` → ON (saved to `WL-SOUND.CFG`; on failure a message is shown and the current RAM sound still works until power-off)
5. Enable silent photography → take a photo → custom shutter sound
6. Use `Preview sound` to preview at any time; after changing files use `Reload sound` to reload

## Flashing

Use the camera's built-in menu update:

1. **First confirm the camera is on official C 2.60**: if the current version is lower than 2.60, download the official C 2.60 firmware package from Nikon, put it in the SD card root, update via `SETUP menu → Firmware version` and finish the official 2.60 upgrade
2. Place this firmware file `eg1630_026000_patch.bin` in the **SD card root**
3. Camera `SETUP menu → Firmware version` → select update → confirm flashing
4. Do not cut power or remove the card during the update; the camera reboots automatically when done
5. Verify: after `SETUP menu → Firmware version` shows the version, the last row of the SETUP menu should show `Shutter sound`

> Restore: put the stock C 2.60 firmware package back on the SD card and flash the official version using the same menu update flow.

## Risks and disclaimer

- **Flashing carries a brick risk**: power loss, interrupted writes, or a wrong file/model may prevent the camera from booting, possibly with no self-recovery
- Flashing **very likely voids the official warranty**; be honest before sending for repair, or restore the stock firmware yourself
- This firmware is a community research project and comes with **no warranty of any kind**; offline validation cannot cover every shooting mode and failure condition, so actual display, file reading and speaker playback are subject to the real device
- An abnormal power loss may leave an invalid `WL-SOUND.CFG`; the next restore rejects that record and stays off, without affecting other camera functions
- To restore: flash back the stock `eg1630_026000.bi` module; settings data is unaffected
