call C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\Anaconda3
call conda create -n cv3 python=3.5.2 -y
call conda activate cv3
call pip install --yes opencv-python
call pip install --yes fire Pillow pypinyin django pandas pymysql

rem call conda deactivate