import cx_Freeze

executables = [cx_Freeze.Executable("SniperGame.py")]

cx_Freeze.setup(
    name="Sniper",
    options={"build_exe":{"packages":["pygame"]}},
    description = "Sniper Game",
    executables = executables
    )
