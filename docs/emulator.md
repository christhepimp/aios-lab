# Rooted Android emulator → Linux shell

## Why this path

Android userland runs on a Linux kernel (goldfish/ranchu in the official emulator). Root on the AVD is root on that guest Linux. That is the door. It is not a new kernel.

## Path A — Android Studio AVD without Play Store

1. Install [Android Studio](https://developer.android.com/studio).
2. Device Manager → Create Device → pick a phone.
3. System image: **Google APIs** (x86_64 or arm64), *not* Google Play.
4. Start the AVD.
5. From the host:

```bash
adb devices
adb root          # restarts adbd as uid 0
adb remount       # writable /system on many images
adb shell
id                 # expect uid=0(root)
uname -a          # Linux ... ranchu or goldfish
```

If `adb root` is denied, you picked a Play Store image. Use Path B or recreate the AVD.

## Path B — Play image + AERoot

Repo: https://github.com/quarkslab/AERoot

```bash
pip install aeroot
emulator @Your_AVD -qemu -s
aeroot daemon     # roots adbd
adb shell         # should be #
```

Requires gdb with Python. Older tool: https://github.com/airbus-seclab/android_emuroot

## What you can see inside

```bash
cat /proc/version
ls /proc/1        # Android init, not systemd
mount
ps -A
```

You are looking at Linux. Replacing files under `/system` is still Android userspace. Replacing the kernel image requires building goldfish/ranchu from AOSP kernel trees and pointing the emulator at it. That is Phase 4+.

## Do not do this on a phone you care about

Emulator only for this lab unless you already know Magisk / KernelSU and accept the blast radius.
