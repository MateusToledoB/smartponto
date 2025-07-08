from cx_Freeze import setup, Executable

build_exe_options = {
    "excludes": ["unittest"],
    "zip_include_packages": ["encodings"],
    "include_files": ["drivers/", "sp.ico"],  # <-- Inclui o ícone e drivers
}

executables = [
    Executable(
        script="gui.py",
        base="Win32GUI",
        icon="sp.ico",           # Ícone do executável (.exe)
        target_name="SmartPonto.exe"
    )
]

setup(
    name="SmartPonto",
    version="0.1",
    description="Automação de Folhas",
    options={"build_exe": build_exe_options},
    executables=executables
)
