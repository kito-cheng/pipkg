import pipkg

pipkg.check_package("pip", update_pip=True)
pipkg.check_package("pip", update_pip=True, always_update=True)
