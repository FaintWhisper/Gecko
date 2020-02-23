@echo off

Title iTunes Tagger

set INPUT_PATH="C:\Users\amit1\Deezloader Music"
set OUTPUT_PATH="C:\Users\amit1\Music"

echo.
echo 						--- iTunes Tagger ---
echo.

cd bin

if %1.==. (
    @echo on

    py tag.py -i %INPUT_PATH% -o %OUTPUT_PATH%
) else (
    @echo on

    py tag.py -i %* -o %OUTPUT_PATH%
)