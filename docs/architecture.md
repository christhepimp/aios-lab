# Architecture

```
+---------------------------------------------+
|  AIOS shell / policy agent   (this repo)    |
|  natural language → allowed host actions    |
+---------------------------------------------+
|  Android userspace  (zygote, binders, apps) |
+---------------------------------------------+
|  Linux kernel (ranchu / goldfish / host)    |
+---------------------------------------------+
|  QEMU / KVM / hypervisor                    |
+---------------------------------------------+
```

Phase 0 only owns the top box. Everything below stays vendor Linux.

## Design rules

1. **Never let the model run raw root commands without a policy gate.**
   `policies/allow.yaml` is the allowlist. Unknown intents refuse.
2. **Observe before you mutate.** First features: `uname`, `ps`, disk, battery via `adb`.
3. **Guest is disposable.** Experiment in the AVD. Snapshot before remount tricks.
4. **PID 1 experiments happen in a nested VM**, not as the emulator's real init, until you can recover from a black screen.

## Non-goals for this repository

- Shipping a custom kernel binary
- Magisk modules for random phones
- Pretending an LLM is a scheduler
- Breaking other people's devices
