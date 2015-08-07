import cx_Freeze

executables = [cx_Freeze.Executable("SniperGame.py")]

cx_Freeze.setup(
    name="Sniper",
    options={"build_exe":{"packages":["pygame"], "include_files":["logo.png","City.png","aim.png","scope.png","targeting.png","criminal.png","shooter.png","left_arrow.png","right_arrow.png","sm_shooter.png","lg_shooter.png","sm_splash.png","lg_splash.png","splatter.png","reload.png","reload2.png","exit.png","exit2.png","return.png","return2.png","sniperShot.wav"]}},
    description = "Sniper Game",
    executables = executables
    )
