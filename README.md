# PIO + ARMCLANG (v6)

## Installation

You need Keil MDK ARM installed of the latest version. Then you should have the path

C:\Keil_v5\ARM\ARMCLANG

copy the `reference_package.json` as `package.json` into this folder.

If your path is different, adapt the `platformio.ini` with regards to the path
```ini
platform_packages = toolchain-armcc@symlink://C:\Keil_v5\ARM\ARMCLANG
```

## Expected Build Results
GCC
```
Linking .pio\build\GCC_genericSTM32F103VC\firmware.elf
Checking size .pio\build\GCC_genericSTM32F103VC\firmware.elf
Advanced Memory Usage is available via "PlatformIO Home > Project Inspect"
RAM:   [          ]   2.3% (used 1152 bytes from 49152 bytes)
Flash: [          ]   1.0% (used 2552 bytes from 262144 bytes)
```
ARMCLANG
```
Linking .pio\build\ARMCC_genericSTM32F103VC\firmware.elf
Checking size .pio\build\ARMCC_genericSTM32F103VC\firmware.elf
Advanced Memory Usage is available via "PlatformIO Home > Project Inspect"
RAM:   [          ]   2.1% (used 1048 bytes from 49152 bytes)
Flash: [          ]   0.8% (used 2140 bytes from 262144 bytes)```
```

## Does it run?

No idea, no HW.