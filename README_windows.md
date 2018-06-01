FacePI for Windows
====================

FacePI 可以移植到 Windows 上囉，已經在 Windows 7 與 Windows 10 實測可行。移植的原因主要是樹莓派的運算效能不夠高，速度慢。因此，若專案不需要使用到 GPIO 控制外部設備的話，安裝在 Windows 上可以找到較好的機器設備運行。

[![Alt text](https://www.youtube.com/upload_thumbnail?v=ORVNkod06pU&t=hqdefault&ts=1527849150645)](https://youtu.be/ORVNkod06pU)


## 搭建環境

### Anaconda
首先必須下載 anaconda ，請選擇 Python3 的版本。安裝完成後，在程式集->anaconda prompt 進入文字介面。

### 建立隔離執行環境
為了避免與原先環境互相衝突，最好的方式就是建立一個隔離的執行環境。接著要安裝什麼都按 [y] 安裝。
    
    conda create -n cv3 python=3.5.2

接著啟用這個環境

    conda activate cv3

在這個隔離環境內安裝 OpenCV

    conda install -c https://conda.anaconda.org/menpo opencv3

如果要脫離這個隔離環境回到 (base)

    conda deactivate

如果要刪除整個隔離環境的話：

    conda remove -n cv3 --all

要看看目前已經存在的環境有哪些：

    conda info -e

進入到 (cv3) 這個環境當中，安裝必要的套件：

    pip install fire 
    pip install Pillow 
    pip install pypinyin

最後，可以開始安裝 FacePI 本體。若您已經安裝 git 環境，則可以直接下以下指令即可。

    git clone https://github.com/jiangsir/FacePI

若沒有 git 指令的話，就直接到 github 把程式抓回來，點擊 Download ZIP。

    https://github.com/jiangsir/FacePI

進入 FacePI 放置的路徑，比如「文件」資料夾

    cd /Users/user/Documents
    # 此處請依據自己的環境修改。 
    
## 執行
執行 FacePI.py, FacePI 主要是一個文字介面程式：


    python FacePI/FacePI.py


    Config: 列出 Config.json 設定。
    Signin: 進行簽到！
    Identify: 用網路 URL 或本地圖片進行辨識。,
    Train: 用 3 連拍訓練一個新人

    Usage:       FacePI.py 
                FacePI.py Config
                FacePI.py Identify
                FacePI.py Signin
                FacePI.py Train


首先，先執行

    python FacePI/FacePI.py Config

可以進行設定，最主要的設定就是 API_KEY 請至微軟網站申請一個 API_KEY。若不修改，直接按 enter 即可使用預設值。

### 訓練
接下來，先進行「訓練」三連拍。用來「訓練」將來要進行辨識的人。

    python FacePI/FacePI.py Train <userData> <姓名>

### 簽到
最後，進行簽到。

    python FacePI/FacePI.py Signin

即可依照畫面指示進行操作。
