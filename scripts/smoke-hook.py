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
    import pyperclip

    sample = "Writing Tools clipboard check — ✓"
    pyperclip.copy(sample)
    assert pyperclip.paste() == sample
    # The launcher must provide a writable persistent directory for settings.
    probe = root / ".write-check"
    probe.write_text("ok")
    probe.unlink()
    print("Frozen imports, Qt, assets, clipboard and writable state passed.", flush=True)
    sys.exit(0)
