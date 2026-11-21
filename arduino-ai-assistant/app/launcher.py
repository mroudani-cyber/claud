"""
Entry point for AI-Assistant.exe.

Runs the newest app code: the copy downloaded by the auto-updater
(%APPDATA%\\AIAssistant\\app\\ai_assistant_app.py) if it is newer and loads
correctly, otherwise the version built into the exe.
"""
import importlib.util
import os
import sys
import traceback

os.environ["AIA_LAUNCHER"] = "1"

import ai_assistant_app as bundled  # noqa: E402  (also makes PyInstaller bundle all dependencies)

LOG = os.path.join(bundled.DATA_DIR, "launcher.log")


def load_updated():
    path = os.path.join(bundled.UPDATE_DIR, "ai_assistant_app.py")
    if not os.path.exists(path):
        return None
    try:
        spec = importlib.util.spec_from_file_location("ai_assistant_app_updated", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if bundled.ver_tuple(mod.APP_VERSION) > bundled.ver_tuple(bundled.APP_VERSION):
            return mod
    except Exception:
        os.makedirs(bundled.DATA_DIR, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("Update failed to load, using built-in version:\n" + traceback.format_exc() + "\n")
    return None


if __name__ == "__main__":
    app = load_updated() or bundled
    try:
        app.main()
    except Exception:
        if app is bundled:
            raise
        # updated code crashed: remember it and fall back to the built-in version
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("Updated version crashed:\n" + traceback.format_exc() + "\n")
        os.replace(os.path.join(bundled.UPDATE_DIR, "ai_assistant_app.py"),
                   os.path.join(bundled.UPDATE_DIR, "ai_assistant_app.broken.py"))
        bundled.main()
