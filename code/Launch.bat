@echo off
set "chemin_fichier=C:\Users\naina\OneDrive\Images\nainaincam 2023\Bot\Pairing_Discord\code\main.py"

:menu
cls
echo 1. Exécuter le fichier Python
echo 2. Arrêter le fichier Python
echo 3. Quitter
set /p choix="Choisissez une option : "

if "%choix%"=="1" (
    py "%chemin_fichier%"
    pause
    goto menu
) else if "%choix%"=="2" (
    taskkill /f /im python.exe /fi "CommandLine like '%%%chemin_fichier%%%'" 2>nul
    echo Fichier Python arrêté.
    pause
    goto menu
) else if "%choix%"=="3" (
    exit
) else (
    echo Choix non valide.
    pause
    goto menu
)
