call C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\Anaconda3
call conda activate cv3
call python %CD%\website\manage.py runserver 0.0.0.0:8000
rem call conda deactivate
pause