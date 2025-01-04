# file is used with textual run --dev

from pathlib import Path
from bagels.locations import set_custom_root

if __name__ == "__main__":
    # set_custom_root(Path("../../../bagels_instance/"))

    from bagels.config import load_config

    load_config()

    from bagels.models.database.app import init_db

    init_db()

    from bagels.app import App

    app = App()
    app.run()
