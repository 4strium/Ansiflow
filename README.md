<div align="center">
	<img src="images/ansiflow.png" alt="Ansiflow" height="160"/>
</div>

<h1 align="center">Ansiflow – 3D ASCII Game Engine & Editor</h1>

Create, configure and play small 3D maze / dungeon experiences fully rendered in ASCII characters.
  
Cross‑platform, open source (GPLv3) and already localized in English & French.

---

## ✨ Features

- **Live editor (PyQt6 GUI)** – map grid, wall tools, enemy placement, NPC configuration.
- **3D ASCII runtime** – launches in an external terminal (ray‑cast style rendering using characters & colors).
- **Project packaging** – all editable data stored under `workingDir/` and exportable to a single `*.ansiflow` archive (zip format).
- **NPC dialogue graph** – block system (start, text, question with branching, regroup / end choice, Python call, end) serialized into NPC data files.
- **Enemy & NPC skins** – generate ASCII art from images (automatic conversion via color sampling).
- **Multilingual** – English / French toggle at startup and changeable later in Parameters (UI text loaded from `language/language_content.json`).
- **Keyboard controls dialog** – shown before starting the game for quick reference.
- **Graceful close workflow** – prompt to save on exit.
- **Consistent branding & icons** – unified window icon (`images/ansiflow-icon.png`).

## 🗂 Repository Layout (Highlights)

```
app.py                  # Main editor window (MainWindow)
main_engine.py          # Runtime ASCII 3D engine (executed in external terminal)
modules/                # Dialogs, tools, widgets (PyQt6)
	starting.py           # Start / project chooser & language selection
   newProject.py         # Create a new project (.ansiflow data skeleton)
	parametersDialog.py   # Rename project + change language at runtime
	commandsDialog.py     # Pre-run controls help
	closeDialog.py        # Save-before-exit dialog
	aboutDialog.py        # About window (logo, version, link)
	... (NPC & block system dialogs)
engine/                 # Lower-level rendering / buffer utilities
scripts/image_to_ascii.py # Image ⇒ ASCII conversion helpers
language/language_content.json # Translation strings
workingDir/             # Current editable project data (generated)
images/, text/, fonts/  # Assets (icons, flags, ASCII art, fonts)
```

## 🔧 Requirements

| Component | Minimum                                                     |
| --------- | ----------------------------------------------------------- |
| Python    | 3.11+ (developed & tested with 3.13)                        |
| OS        | Windows / macOS / Linux (X11 / Wayland)                     |
| Terminal  | Must support ANSI escape codes & 24‑bit color for best look |

Python dependencies (install manually if you do not already have them):

```
pip install PyQt6 Pillow
```

> Pillow is required for image → ASCII conversion. No database or network dependencies.

## 🚀 Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/4strium/Ansiflow.git
   cd Ansiflow
   ```
2. Install dependencies (virtual environment recommended):
   ```
   python -m venv .venv
   # Windows PowerShell
   .venv\\Scripts\\Activate.ps1
   # macOS / Linux
   source .venv/bin/activate
   pip install PyQt6 Pillow
   ```
3. Launch the editor:
   ```
   python app.py
   ```
4. Choose language, create a new project OR load an exported `*.ansiflow` file.
5. Configure map, player spawn, enemies, exit tile, NPCs (dialogue blocks + skins).
6. Press Ctrl+E or use Menu → Execution → Start your game.
7. Review controls dialog, then the external ASCII 3D view launches.

## 💾 Project Files & Export

- Working state lives in `workingDir/` (JSON data + generated NPC text + temporary assets).
- Export: Menu → File → Save (or Save as…) creates / overwrites a `*.ansiflow` archive.
- Import: From the start window “Load Project” (`*.ansiflow` is simply an uncompressed zip you can inspect if needed).

## 🧩 NPC Dialogue System (Overview)

Each NPC dialogue is built from draggable blocks:

- Start (entry point)
- Text (shows a line with a chosen skin)
- Question (player choices; branching)
- Regroup / EndChoice (collect branch endings)
- Python Call (invoke a function name placeholder in future extensions)
- End (terminal block)

Dialogue graphs are serialized when you export or launch the game. Validation ensures all required paths (start/end, skins, positions) are set before play.

## 🌐 Localization

All UI strings are in `language/language_content.json`. Add a new locale by:

1. Duplicating the key structure.
2. Adding a language selector entry in `starting.py` & `parametersDialog`.
3. Updating any logic that infers available language codes.

Runtime switching calls `MainWindow.updateInterfaceTexts()` to refresh labels and menus.

## 🖼 Skins & ASCII Conversion

Enemy and NPC skins are derived from user‑selected images. The converter downsamples and maps color blocks to ASCII, producing text files consumed by the engine. Larger images may increase processing time; prefer small, high‑contrast sources.

## 🛠 Troubleshooting

| Issue                                          | Cause / Fix                                                                                   |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Game launch blocked (warnings)                 | Ensure player spawn, enemy skin, and exit tile are all defined.                               |
| Window text not updating after language change | Reopen dialogs; core window updates via `updateInterfaceTexts()`.                             |
| Image conversion slow                          | Use smaller images; avoid very large PNG/JPG files.                                           |
| Terminal colors look dull                      | Use a truecolor (24‑bit) capable terminal (Windows Terminal, iTerm2, modern Linux terminals). |

## 🤝 Contributing

1. Fork & branch (`feat/your-topic`).
2. Keep PRs focused & documented (screenshots / GIFs welcome).
3. Ensure English strings & add FR versions if adding UI text.
4. Respect code style (follow existing spacing & naming).

## 📜 License

Released under the **GNU GPLv3** (see `LICENSE`). You may copy, modify and distribute under the same license. No warranty.

## 🙌 Credits

Project author: 4strium.

Libraries: PyQt6, Pillow.

Logo & assets: Stored under `images/` (see repository history for origins where applicable).

---

<sub>Ansiflow is experimental software. Feedback & issues welcome via GitHub.</sub>
