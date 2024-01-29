@echo off
echo 准备粉碎 "%CD%"，确定吗？
timeout /t 10 /nobreak
for /r %%i in (*) do (
    if not "%%~pi"=="%CD%\" move "%%i" "%CD%"
)
