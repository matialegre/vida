@echo off
REM Turno noche LOCAL - corre en la PC de Matias, pushea de verdad (git local con permiso de escritura)
cd /d "C:\Users\Pandemonium\Documents\MATI-HQ"
echo ===== TURNO NOCHE %DATE% %TIME% ===== >> "scripts\turno_noche_log.txt"
type "scripts\turno_noche_prompt.md" | "C:\Users\Pandemonium\.local\bin\claude" --print --dangerously-skip-permissions --model opus >> "scripts\turno_noche_log.txt" 2>&1
echo ===== FIN %DATE% %TIME% ===== >> "scripts\turno_noche_log.txt"
