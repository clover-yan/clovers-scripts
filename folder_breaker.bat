@echo off
echo ׼������ "%CD%"��ȷ����
timeout /t 10 /nobreak
for /r %%i in (*) do (
    if not "%%~pi"=="%CD%\" move "%%i" "%CD%"
)
