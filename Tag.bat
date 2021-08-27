@echo off

Title Gecko: Music Tagger

:: Change these paths according to your needs
set INPUT_PATH="C:\Users\amit1\Downloads"
set OUTPUT_PATH="C:\Users\amit1\Music"

if %1.==. (
    @echo on

    py src/tag.py -i %INPUT_PATH% -o %OUTPUT_PATH%
) else (
    @echo on

    py src/tag.py -i %* -o %OUTPUT_PATH%
)

@echo off
timeout /t 2 /nobreak > NUL