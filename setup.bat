setlocal enableextensions enabledelayedexpansion


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

call conda remove -n cv3 --all -y
call conda create -n cv3 python=3.5.2 -y
call conda activate cv3
rem call conda install -c menpo opencv3 -y

python -m pip install --upgrade pip
rem rem opencv 4.00
call pip install opencv-python==3.2.0.8

call pip install cython msgpack fire Pillow pypinyin django pandas pymysql numpy scipy scikit-image cmake imutils

rem dlib
pip install dlib==18.17.100
pip install dlib

rem
rem pip install imutils

rem call conda deactivate
pause

