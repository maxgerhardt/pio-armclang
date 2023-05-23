import os
from SCons.Script import Import, Builder

Import("env")
Import("projenv")
platform = env.PioPlatform()

# Filter out excluded build options from flag variable
def FilterFlags(flagVar, filteredOptions):
    filteredFlags = [flag for flag in flagVar if flag not in filteredOptions]
    return filteredFlags

# Define list of flag variables for option exclude
filteredBuildFlags = ["CPPFLAGS", "CFLAGS", "CCFLAGS", "CXXFLAGS", "ASFLAGS", "LINKFLAGS", "_LIBFLAGS"]

# Define default flags to exclude from all flag variables
filteredOptions = [
    "-Wall",
    "-ffunction-sections",
    "-fdata-sections",
    "-mcpu=cortex-m3",
    "-Os",
    "nostdlib",
    "-l",
    "-mthumb",
    "-Wl,--gc-sections,--relax",
    "-specs=nano.specs",
    "-l,--gc-sections,--relax",
    # Add more flags to exclude as needed
]

# Use ARMCC for framework
for e in [env, projenv, DefaultEnvironment()]:

    e.Replace(
        AR = "armar",
        AS = "armclang",
        CC = "armclang",
        CXX = "armclang",
        LD = "armlink",
        # SCons oddity: This points to $SMARTLINK by default, a function that will return $CXX as the linker
        # this is however not possible in this toolchain's case
        LINK= "armlink",
        GDB = "arm-none-eabi-gdb",  # to retain compatibility
        
        # we can't seem to be able to alter the command string used in
        # the ElfToBin / ElfToHex builders in this script. weird.
        # This is a **extremely crude hack** that injects the right command
        OBJCOPY = "fromelf --bin --output $TARGET $SOURCE && echo ",
        #SIZE = "armsize",
        SIZEPROGREGEXP=r"^(?:ER_IROM1)\s+(\d+).*",
        SIZEDATAREGEXP=r"^(?:RW_IRAM1)\s+(\d+).*",
    )

    # Remove GCC "-Wl" options completely
    e.Replace(_LIBFLAGS = [])

    e.Append(CPPFLAGS = [
        "-DUSE_HAL_DRIVER",
        "-DSTM32F103xE",
        "-DUSER_VECT_TAB_ADDRESS",
        # Add more flags to exclude as needed
    ])

    e.Append(CCFLAGS = [
        #"--c99",
        "--target=arm-arm-none-eabi",
        #"-c",
        "-mcpu=Cortex-M3",
        "-g",
        "-O0",
        #"-M",
        "-mthumb",
        #"--apcs=interwork",
        #"-o C:\\Users\\gacnik\\Desktop\\PVC2-SES-PlatformIO\\PVC2 test\\.pio\\build\\genericSTM32F103VC\\src\\Drivers\\STM32F1xx_HAL_Driver\\Src"
        # Add more flags to exclude as needed
    ])

    e.Append(ASFLAGS = [
        "--target=arm-arm-none-eabi",
        "-mcpu=Cortex-M3",
        "-g",
        "-masm=auto",
        "-c",
        "-D__MICROLIB"
        #"--apcs=interwork",
        #"-M",
        # Add more flags to exclude as needed
    ])

    e.Append(LINKFLAGS = [
        "--library_type=microlib",
        "--strict",
        #"--target=arm-arm-none-eabi",
        #"-mcpu=Cortex-M3",
        # "-o C:\\Users\\gacnik\\Desktop\\PVC2-SES-PlatformIO\\PVC2 test\\.pio\\build\\genericSTM32F103VC\\src\\Drivers\\STM32F1xx_HAL_Driver\\Src"
        # Add more flags to exclude as needed
    ])
    old_flags = e["LINKFLAGS"].copy()
    # replace "-T" with "--scatter" for linker scirpt
    try:
        i = old_flags.index("-T")
        #print("INDEX:  " + str(i))
        old_flags[i] = "--scatter"
        e.Replace(LINKFLAGS=old_flags)
    except:
        pass

    e.Replace(LIBPATH=[]) # no library paths for now that would generate -L flags

    # Filter out excluded flags from all flag variables
    for flag in filteredBuildFlags:
        existingFlags = e.get(flag, [])
        filteredFlags = FilterFlags(existingFlags, filteredOptions)
        e.Replace(**{flag: filteredFlags})

    # Add to path.. somehow PlatformIO does not do this although it's the toolchain package.
    pkg = platform.get_package("toolchain-armcc")
    e.PrependENVPath(
        "PATH",
        os.path.join(pkg.path, "bin")
        if os.path.isdir(os.path.join(pkg.path, "bin"))
        else pkg.path,
    )