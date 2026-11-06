"""Optional frozen application check used only by the container build."""
import os

if os.environ.get("WRITING_TOOLS_SMOKE_TEST") == "1":
    import sys
    from pathlib import Path

    import WritingToolApp
    from PySide6.QtGui import QPixmap
    from PySide6.QtWidgets import QApplication

    app = QApplication([])
    root = Path(sys.executable).parent
    assert (root / "options.json").is_file()
    assert (Path(sys._MEIPASS) / "locales").is_dir()
    assert not QPixmap(str(root / "background.png")).isNull()
    print("Frozen Writing Tools imports, Qt and assets passed.", flush=True)
    sys.exit(0)
