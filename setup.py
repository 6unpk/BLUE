from cx_Freeze import setup, Executable

setup(
    name ="BLUE",
    version = "1.0",
    description ="BLUE is normal the Rhythm Game",
    executables = [Executable("main.py")]

)
