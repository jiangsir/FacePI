setlocal enableextensions enabledelayedexpansion
set CONDA_NAME=cv31
IF EXIST %ALLUSERSPROFILE%\Anaconda3\ (
call %ALLUSERSPROFILE%\Anaconda3\Scripts\activate.bat %ALLUSERSPROFILE%\Anaconda3
set ANACONDA_PATH=%ALLUSERSPROFILE%\Anaconda3
echo alluser
) ELSE (
call %HomeDrive%%HomePath%\Anaconda3\Scripts\activate.bat %HomeDrive%%HomePath%\Anaconda3
set ANACONDA_PATH=%HomeDrive%%HomePath%\Anaconda3
echo one user
)
SET PATH=%PATH%;%ANACONDA_PATH%;%ANACONDA_PATH%\Scripts\;

call conda activate %CONDA_NAME%
where python
python --version
python %CD%\FacePI.py Signin

pause