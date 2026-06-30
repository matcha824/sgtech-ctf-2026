@echo off
echo ========================================
echo Two-Time Pad Challenge Automated Setup
echo ========================================
echo.

REM Step 1: Generate pad.png
echo [Step 1] Generating pad.png (1024x576) in RGB mode...
python generate_pad.py
if errorlevel 1 (
    echo Error generating pad.png
    exit /b 1
)
echo.

REM Step 2: XOR pad.png with flag.png
echo [Step 2] XORing pad.png with flag.png...
python xor_images.py pad.png flag.png picture_1.png
if errorlevel 1 (
    echo Error XORing pad.png with flag.png
    exit /b 1
)
echo.

REM Step 3: XOR pad.png with other_img.png
echo [Step 3] XORing pad.png with other_img.png...
python xor_images.py pad.png other_img.png picture_2.png
if errorlevel 1 (
    echo Error XORing pad.png with other_img.png
    exit /b 1
)
echo.

REM Step 4: XOR picture_1.png with picture_2.png to ensure solution validates
REM Mainly a sanity check to ensure the challenge is solvable
echo [Step 4] XORing picture_1.png with picture_2.png to ensure solution validates...
python xor_images.py picture_1.png picture_2.png solution.png
if errorlevel 1 (
    echo Error XORing picture_1.png with picture_2.png
    exit /b 1
)
echo.

echo ========================================
echo Finished setup!
echo Please ensure solution.png is valid
echo ========================================
