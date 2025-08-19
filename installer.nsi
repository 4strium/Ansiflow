; ============================
; Ansiflow Installer (Modern UI)
; ============================
Unicode True
OutFile "AnsiflowSetup.exe"
Name "Ansiflow"
InstallDir "$PROGRAMFILES\Ansiflow"
RequestExecutionLevel admin

; ------------ Configuration ------------
!define PRODUCT_NAME "Ansiflow"
!define PRODUCT_VERSION "0.1.0"           
!define PRODUCT_VERSION_NUM "0.1.0.0"
!define PRODUCT_PUBLISHER "Romain M."
!define PRODUCT_URL "https://github.com/4strium/Ansiflow" 
!define UNINSTALL_KEY "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${PRODUCT_NAME}"
!define ICON_PATH "images\\ansiflow-icon.ico" ; Chemin de l'icône (présent dans dossier images)

; ------------ Modern UI 2 ------------
!include "MUI2.nsh"

!define MUI_ABORTWARNING
!define MUI_ICON "${ICON_PATH}"
!define MUI_UNICON "${ICON_PATH}"
!define MUI_WELCOMEFINISHPAGE_BITMAP "images\\ansiflow-header.bmp"
!define MUI_WELCOMEPAGE_TITLE "${PRODUCT_NAME} v${PRODUCT_VERSION}"
!define MUI_WELCOMEPAGE_TEXT "Assistant d'installation de ${PRODUCT_NAME}."
!define MUI_FINISHPAGE_TITLE "Installation terminée"
!define MUI_FINISHPAGE_RUN "$INSTDIR\\Ansiflow.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Lancer ${PRODUCT_NAME} maintenant"
!define MUI_FINISHPAGE_LINK "Projet / Support"
!define MUI_FINISHPAGE_LINK_LOCATION "${PRODUCT_URL}"

BrandingText "${PRODUCT_NAME} v${PRODUCT_VERSION} - par ${PRODUCT_PUBLISHER}"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "French"
!insertmacro MUI_LANGUAGE "English"

; ------------ Version Resource (EXE metadata) ------------
VIProductVersion "${PRODUCT_VERSION_NUM}"
VIAddVersionKey "ProductName" "${PRODUCT_NAME}"
VIAddVersionKey "FileDescription" "${PRODUCT_NAME} Installer"
VIAddVersionKey "CompanyName" "${PRODUCT_PUBLISHER}"
VIAddVersionKey "FileVersion" "${PRODUCT_VERSION}" 
VIAddVersionKey "ProductVersion" "${PRODUCT_VERSION}" 
VIAddVersionKey "OriginalFilename" "AnsiflowSetup.exe"
VIAddVersionKey "Homepage" "${PRODUCT_URL}"
VIAddVersionKey "LegalCopyright" "© 2025 ${PRODUCT_PUBLISHER}"

; ----------------------------
; Installation Section
; ----------------------------
Section "Install Ansiflow"
    ; Root path
    SetOutPath "$INSTDIR"

    ; Main executable
    File "Ansiflow.exe"

    ; Copy asset directories (preserve folder names)
    File /r "_internal"
    File /r "language"
    File /r "images"
    File /r "text"
    File /r "fonts"
    File /r "workingDir"

    ; Create Start Menu folder & shortcuts
    CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
    CreateShortcut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" "$INSTDIR\Ansiflow.exe"
    CreateShortcut "$DESKTOP\${PRODUCT_NAME}.lnk" "$INSTDIR\Ansiflow.exe"

    ; Write uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ; Registry (Add/Remove Programs)
    WriteRegStr HKLM "${UNINSTALL_KEY}" "DisplayName" "${PRODUCT_NAME}"
    WriteRegStr HKLM "${UNINSTALL_KEY}" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "${UNINSTALL_KEY}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "${UNINSTALL_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
    WriteRegStr HKLM "${UNINSTALL_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
    WriteRegStr HKLM "${UNINSTALL_KEY}" "URLInfoAbout" "${PRODUCT_URL}"
SectionEnd

; ----------------------------
; Uninstall Section
; ----------------------------
Section "Uninstall"
    Delete "$DESKTOP\${PRODUCT_NAME}.lnk"
    Delete "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk"
    RMDir /r "$SMPROGRAMS\${PRODUCT_NAME}"
    RMDir /r "$INSTDIR"
    DeleteRegKey HKLM "${UNINSTALL_KEY}"
SectionEnd