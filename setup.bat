call C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\Anaconda3
call conda create -n cv3 python=3.5.2 -y
call conda activate cv3
rem opencv 4.00 前的最後一版
call pip install opencv-python=3.4.5.20
call pip install fire Pillow pypinyin django pandas pymysql numpy scipy scikit-image cmake dlib imutils

rem dlib 另一個安裝版本
rem pip install pip install dlib==18.17.100
rem 處理圖片
rem pip install imutils

rem call conda deactivate