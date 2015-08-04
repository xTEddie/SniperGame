import cx_Freeze

executables = [cx_Freeze.Executable("SniperGame.py")]

cx_Freeze.setup(
    name="Sniper",
    options={"build_exe":{"packages":["pygame"], "include_files":["logo.png","City.png","aim.png","scope.png","left_arrow.png","right_arrow.png","sm_criminal.png","lg_criminal.png","sm_splash.png","lg_splash.png","sniperShot.wav"]}},
    description = "Sniper Game",
    executables = executables
    )
