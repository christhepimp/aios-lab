# AIOS Lab

Research workspace for an **AI-native operating layer**.

The long-term idea: the OS itself reasons — it does not just run programs.  
The short-term reality: Android and every practical emulator still sit on a **Linux kernel**. You do not delete Linux in one weekend. You sit *on* it, then slowly own more of the stack.

This repo is that first layer.

## What this is (and is not)

**Is**
- A lab for a rooted Android emulator + Linux userspace
- A userspace *AI shell* that can become the default interface
- Notes for later: init replacement, policy daemon, optional custom kernel modules

**Is not**
- A drop-in Linux replacement
- A finished kernel
- A claim that the OS is now an AI after cloning this repo

Replacing `init`, the scheduler, and the kernel is multi-year systems work (AOSP, Fuchsia, seL4, Redox). Start where every real project starts: a machine you control, a root shell, and a process that *looks like* the OS to the user.

## Recommended emulator path (root + Linux inside)

Android *is* Linux plus a userspace. Inside a rooted emulator you already have a Linux kernel, `adb shell`, and `/system`.

### 1. Best default: Android Studio AVD (Google APIs, not Play Store)

Play Store images lock `adbd`. Google APIs / AOSP images usually allow:

```bash
adb root
adb remount
adb shell
# prompt becomes #  — uid 0
```

That is a real Linux root shell on the guest kernel.

### 2. Play Store AVD: AERoot

If you need Play services: [quarkslab/AERoot](https://github.com/quarkslab/AERoot) grants root on-the-fly via QEMU gdb (`emulator @AVD -qemu -s`). Modes: `pid`, `name`, `daemon` (roots `adbd` so every `adb shell` is root).

Predecessor: [airbus-seclab/android_emuroot](https://github.com/airbus-seclab/android_emuroot).

### 3. Genymotion

Developer emulator; many images can be rooted dynamically. Good for QA, not for rewriting the kernel.

### 4. Waydroid (Linux host)

Android in an LXC container sharing the host kernel. Root is easier; you are still on Linux.

### 5. Full custom OS later

[AOSP](https://source.android.com/) + goldfish/ranchu kernel if you want to change Android itself. That is compiling Android from source, not replacing Linux with AI.

Gaming emulators (BlueStacks, LDPlayer, Nox) can be rooted with vendor tools but are a poor lab for kernel work.

## The replacement plan (slow on purpose)

```
Phase 0  You are here
         Rooted emulator + adb + this repo's AI shell in userspace

Phase 1  AIOS as login / default shell
         Replace interactive surface. Kernel untouched.

Phase 2  Supervisory daemon
         Watch processes, storage, network. Policy in natural language to syscalls.

Phase 3  Custom init (userspace PID 1 experiment in a VM, not on the host)

Phase 4  Optional kernel modules / eBPF for observation only

Phase 5  Research: capability microkernel or unikernel beside Linux
         (Fuchsia-style, seL4 guest, Firecracker). Not a wholesale rm -rf /.
```

"The OS is an AI" at Phase 1 means: the thing you talk to is an agent that owns session policy. Hardware, drivers, and scheduling stay Linux until much later.

## Repo layout

```
docs/emulator.md     how to get a rooted Linux shell in an AVD
docs/architecture.md stack diagram and non-goals
shell/aios.py        Phase-0 AI shell (userspace)
policies/            example intent to action rules
```

## Quick start (host Linux or WSL)

```bash
python3 shell/aios.py
```

On the emulator after root, drive the guest from the host with `adb`. Most AVDs do not ship CPython.

## Safety

This lab is for your emulator and your VMs. Do not use root tooling against devices you do not own. Do not treat an LLM as privileged init on a machine that matters.

## License

MIT — see LICENSE.
