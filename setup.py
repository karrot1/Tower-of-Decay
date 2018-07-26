from cx_Freeze import setup, Executable

base = None

executables = [Executable("engine.py", base=base,targetName="towerofdecay.exe")]

packages = ["libtcodpy", "copy", "shelve", "os", "dbm"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "Tower of Decay",
    options = options,
    version = "0.2.1",
    description = 'Tower of Decay',
    executables = executables
)