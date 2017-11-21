;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

SetCompressor /SOLID lzma
!define MUI_ICON "pwcalculator.ico"
!define MUI_PRODUCT "Password Calculator"

;--------------------------------
;General

  Unicode true

  ;Name and file
  Name "${MUI_PRODUCT}"
  OutFile "${MUI_PRODUCT} Setup.exe"
  BrandingText "bixense.com/pwcalculator"

  ;Default installation folder
  InstallDir "$LOCALAPPDATA\Programs\${MUI_PRODUCT}"

  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\${MUI_PRODUCT}" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel user

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES

  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES

  !define MUI_FINISHPAGE_RUN "$INSTDIR\pwcalculator.exe"
  !insertmacro MUI_PAGE_FINISH

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Reserve Files

  ;If you are using solid compression, files that are required before
  ;the actual installation should be stored first in the data block,
  ;because this will make your installer start faster.

  !insertmacro MUI_RESERVEFILE_LANGDLL

;--------------------------------
;Installer Sections

Section "" SecUninstallPrevious
  Call UninstallPrevious
SectionEnd

Section ""

  Call UninstallPrevious

  SetOutPath "$INSTDIR"

  File C:\msys64\mingw64\bin\libstdc++-6.dll
  File C:\msys64\mingw64\bin\wxbase30u_gcc_custom.dll
  File C:\msys64\mingw64\bin\wxmsw30u_core_gcc_custom.dll
  File C:\msys64\mingw64\bin\libgcc_s_seh-1.dll
  File C:\msys64\mingw64\bin\libwinpthread-1.dll
  File C:\msys64\mingw64\bin\zlib1.dll
  File C:\msys64\mingw64\bin\libjpeg-8.dll
  File C:\msys64\mingw64\bin\libpng16-16.dll
  File C:\msys64\mingw64\bin\libtiff-5.dll
  File C:\msys64\mingw64\bin\liblzma-5.dll
  File ..\..\build\pwcalculator.exe

  CreateShortcut "$desktop\${MUI_PRODUCT}.lnk" "$instdir\pwcalculator.exe"

  ;Store installation folder
  WriteRegStr HKCU "Software\${MUI_PRODUCT}" "" $INSTDIR

  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}" \
                   "DisplayName" "${MUI_PRODUCT}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}" \
                   "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}" \
                   "DisplayIcon" "$INSTDIR\pwcalculator.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}" \
                   "Publisher" "Bixense"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}" \
                   "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
  WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

Function UninstallPrevious

  DetailPrint "Checking"
  ; Check for uninstaller.
  ReadRegStr $R0 HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}" \
                      "QuietUninstallString"

  ${If} $R0 == ""
    Goto Done
  ${EndIf}

  DetailPrint "Removing previous installation."

  ; Run the uninstaller silently.
  ExecWait $R0

  Done:

FunctionEnd

;--------------------------------
;Installer Functions

Function .onInit

  !insertmacro MUI_LANGDLL_DISPLAY

FunctionEnd

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  Delete "$INSTDIR\Uninstall.exe"
  Delete "$desktop\${MUI_PRODUCT}.lnk"

  RMDir /r "$INSTDIR"

  DeleteRegKey /ifempty HKCU "Software\${MUI_PRODUCT}"
  DeleteRegKey /ifempty HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}"

SectionEnd

;--------------------------------
;Uninstaller Functions

Function un.onInit

  !insertmacro MUI_UNGETLANGUAGE

FunctionEnd
