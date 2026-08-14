# WorkRestore

**WorkRestore** is a Windows desktop application that lets you save your current working environment and restore it later.

Instead of reopening your applications, folders, and projects one by one, WorkRestore saves them as a workspace and restores the saved environment when you need it again.

## ✨ Features

* 💻 Save currently running user applications
* 🔄 Restore saved applications
* 📄 Restore exact Microsoft Office documents

  * Microsoft Word
  * Microsoft Excel
  * Microsoft PowerPoint
* 📝 Restore Notepad
* 🧑‍💻 Restore VS Code workspaces
* 📁 Restore File Explorer folders
* 💾 Save workspaces as JSON
* 🗑️ Delete saved workspaces
* 🪟 Windows desktop application
* 📦 Windows installer included
* 🎨 Custom WorkRestore application icon

## 🚀 How It Works

### 1. Open WorkRestore

Launch WorkRestore on your Windows PC.

### 2. Refresh Workspace

WorkRestore detects the supported applications, folders, and VS Code workspaces currently being used.

### 3. Save Workspace

Give your workspace a name, for example:

```text
Work Project
```

WorkRestore saves the workspace information in JSON format.

### 4. Restore Workspace

Select a saved workspace and click **Restore**.

WorkRestore opens the applications, folders, VS Code projects, and saved Office documents from that workspace.

## 📄 Office Document Restore

WorkRestore can save the exact path of supported Office documents.

For example:

```text
Microsoft Excel
C:\Users\User\Documents\Book1.xlsx
```

When the workspace is restored, WorkRestore launches Excel with the saved document.

The same approach is supported for Word and PowerPoint documents.

## 🧑‍💻 VS Code

WorkRestore can save a VS Code workspace/project path.

Example:

```text
C:\Users\User\Desktop\MyProject
```

When restored, WorkRestore launches VS Code with the saved project.

## 📁 File Explorer

Open File Explorer folders can also be saved as part of a workspace.

When the workspace is restored, WorkRestore reopens the saved folders.

## 💾 Workspace Storage

Saved workspaces are stored as JSON files.

Example:

```text
data/
└── workspaces/
    └── Work-Project.json
```

A workspace contains information such as:

```json
{
    "name": "Work-Project",
    "applications": [],
    "explorer_windows": [],
    "vscode_windows": []
}
```

## 📥 Installation

### Option 1 — Installer

Download the latest WorkRestore installer from the GitHub Releases page.

**Download:**
https://github.com/dv-ankits102/WorkRestore/releases/latest

Run:

```text
WorkRestore-Setup-v1.0.0.exe
```

Then follow the Windows installation wizard.

### Option 2 — Run from Source

Clone the repository:

```bash
git clone https://github.com/dv-ankits102/WorkRestore.git
```

Open the project:

```bash
cd WorkRestore
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run WorkRestore:

```bash
python app/main.py
```

## 🛠️ Tech Stack

* Python
* PySide6
* psutil
* pywin32
* JSON
* PyInstaller
* Inno Setup

## 🪟 Platform

Currently supported:

**Windows**

## 🔒 Privacy

WorkRestore is designed to save workspace information locally on the user's computer.

Workspace data is stored locally as JSON files.

No cloud account is required for the core workspace save and restore functionality.

## 📌 Version

**WorkRestore v1.0.0**

## 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

## 🔗 Links

**GitHub Repository:**
https://github.com/dv-ankits102/WorkRestore

**Download Latest Release:**
https://github.com/dv-ankits102/WorkRestore/releases/latest

---

Made with ❤️ for Windows productivity.
