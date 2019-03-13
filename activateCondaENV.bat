setlocal enableextensions enabledelayedexpansion

set CONDA_NAME=cv31

IF EXIST %ALLUSERSPROFILE%\Anaconda3\ (
call %ALLUSERSPROFILE%\Anaconda3\Scripts\activate.bat %ALLUSERSPROFILE%\Anaconda3
set ANACONDA_PATH=%ALLUSERSPROFILE%\Anaconda3
echo alluser
) ELSE (
    IF EXIST %HomeDrive%%HomePath%\Anaconda3\ (
        call %HomeDrive%%HomePath%\Anaconda3\Scripts\activate.bat %HomeDrive%%HomePath%\Anaconda3
        set ANACONDA_PATH=%HomeDrive%%HomePath%\Anaconda3
        echo one user
    ) ELSE (
        echo Please INSTALL Anaconda First!
    )
)

SET PATH=%PATH%;%ANACONDA_PATH%;%ANACONDA_PATH%\Scripts\;

