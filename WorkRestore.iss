#define MyAppName "WorkRestore"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "WorkRestore"
#define MyAppExeName "WorkRestore.exe"

[Setup]
AppId={{8D9E6B8C-7A6A-4F9E-B9D5-WorkRestore100}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\WorkRestore
DefaultGroupName={#MyAppName}

OutputDir=installer
OutputBaseFilename=WorkRestore-Setup-v1.0.0

Compression=lzma
SolidCompression=yes

ArchitecturesInstallIn64BitMode=x64compatible

SetupIconFile=C:\Users\hp\Desktop\WorkRestore\workrestore.ico
UninstallDisplayIcon={app}\WorkRestore.exe

PrivilegesRequired=lowest

DisableProgramGroupPage=yes
WizardStyle=modern

[Files]
Source: "C:\Users\hp\Desktop\WorkRestore\dist\WorkRestore\*"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autodesktop}\WorkRestore"; \
    Filename: "{app}\WorkRestore.exe"; \
    IconFilename: "{app}\WorkRestore.exe"

Name: "{group}\WorkRestore"; \
    Filename: "{app}\WorkRestore.exe"; \
    IconFilename: "{app}\WorkRestore.exe"

[Run]
Filename: "{app}\WorkRestore.exe"; \
    Description: "Launch WorkRestore"; \
    Flags: nowait postinstall skipifsilent