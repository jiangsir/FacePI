FacePI for Windows
====================

2017 年可說是各種刷臉應用的爆發的一年，各種應用目不暇給。微軟也在 2016 年提出「微軟認知服務」，裡面就包含了一組 API ，叫做 Face API，專門提供臉部辨識服務，FacePI 就是利用這個 Face API 設計成一個刷臉簽到應用。

在這裡要先做一些名詞解釋，因為中文裡面這幾個詞有點容易搞混。
* 「臉部偵測(Face Detection)」:偵測影像中的一或多張人臉，並取得影像臉部位置所在的臉部矩形及臉部屬性，該屬性內含以機器學習為基礎的臉部特徵預測。可用的臉部屬性功能 包括：年齡、表情、性別、姿勢、微笑及鬍子，以及影像中每張臉部的 27 個地標。
* 「臉部驗證(Face Verification)」:檢查兩張臉部是屬於同一個人的可能性。API 會傳回信心分數，顯示兩張臉部是屬於同一個人的可能性。
* 「表情辨識」：臉部 API 現在與表情辨識整合，並傳回影像中每個臉部之一組表情的信心分數，例如生氣、藐視、厭惡、恐懼、快樂、不表意見、憂傷及驚奇。這些表情已知可跨文化普遍地與特定臉部表情溝通。
* 「臉部辨識(Face Identification)」:臉部 API 讓您可搜尋、識別和比對您私人存放庫中多達 1 百萬人的臉部。

2018年5月 FacePI 已經跨平台至 Windows 上囉，已經在 Windows 7 與 Windows 10 實測可行。移植的原因主要是樹莓派的運算效能不夠高，速度慢。因此，若專案不需要使用到 GPIO 控制外部設備的話，安裝在 Windows 上可以找到較好的機器設備運行。

點擊播放影片

[![Alt text](https://i.ytimg.com/vi/ORVNkod06pU/hqdefault.jpg)](https://youtu.be/ORVNkod06pU)


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


首先，請務必先進行系統設定，指令如下：

    python FacePI/FacePI.py Config

可以進行設定，最主要的設定就是 API_KEY 請至微軟網站申請一個 API_KEY。
進入到微軟官方頁面 [試用辨識服務](https://azure.microsoft.com/zh-tw/try/cognitive-services/?api=face-api)，我們要的是 臉部 API 點擊取得 API 金鑰。然後你就可以獲得 30 天的試用，總共 30000 筆查詢，每分鐘上限 20 筆。對於實驗來說夠用了。但如果要實際使用，每一個月要重新來一次也真是夠煩的。
因此，比較好的作法是，申請 Azure 帳號，一申請就送你 200 美金的用量，也足以做一個小型應用了，並且 API_KEY 也不會過期。至於用量同樣有每分鐘上限 20 筆，每月 30000 筆查詢的用量，若真的不夠，就可以在後台「儀表板」改為付費模式。每 1000 筆查詢大約會產生 1 美元的費用。
![計費方案](https://lh3.googleusercontent.com/4fWGuNtB_qD2N6V0NciDYlYRqQWjdr9kINpSy1hplINrf9E_uuWm3tzLs2v5UkjZXwJXgodRq7-ixzdjTWrmXHV8-xmQqEFcKKg2pcTcKKBRPHvbB5N23xF3tiFXjDyRJ1z8okpTwHObv7U66Jzr0QjQV4KMjEGhpxAUYGD_QOSmJFzqCSq4cdmMiD2EyScbxv2OPFAk6KWLUlxSC6qnkRh-tcfq0oAkfD1npoA0GZE-Lp7IxdlIGp2sQVhc57UWBah5JpZfNZ8SiGyazHTtOYuO9eO49nrSa-5V9SjvPieFULGLRSOqsJiCuwklBxqN7A9thB_KbVtZKKHVFZqSqgKF_v6Z8l7l1o0zcbQTc_oabNcSLspSuT9roVY5d1346QPAAviizXFRgD19wjirNeNMIGPHSDddEimHmjKPHQU0wQVn_4luKEaXe_2h6NKz-pIsAUCU5Bgc73PvROr7AnQTvrpx1_xjQHVW_TbpoLR95-3xYWxOSw-YfhzJFcM-HZJxxEfAXM1fPuUWpm_33yX5xySRZxDt4oB27aIm7SWAcVqjXaaCow4DdyPyQA5I3rpkXYtu9mJth2OG0KoCZNBH9RXPRnyaDPx_a_fNwxp1Yn7a_XoMoH9w_e4_ZUzBmRtTTPHwrvGWb1EqIgYlpq82soPoZkN5=w430-h440-no)

為了推廣人工智慧應用，諸位軟體大咖們真的是拚了。

![計量圖表](https://lh3.googleusercontent.com/20ZauFmnXnugCGQaZCsdcnMWCb9iXzUNmMvJVXZ91f-5yDacrE1fYItoGJUv1fCqiaaDuvrp4-tp_eUltCxDX75rMjG5TK3v5GFxNr45s9KG2YYtS5x5s9lqK1LhOXu4sLmA1gkINyQhF6Y5lBiFE3tYubcqrJ2s8XQwDrI12paGVRNYtOFqrXhtYv7rFn1zgilx3M32hR5m5UETB6dEkwQEZDnZ1NGHQbbzQVW79M4cplKYm0OLjlYZBVltsU3_-LkQLG7elm10DlIShuWJmAlbO4QXehQry2RC202k7lNoiW2SoQhjPiOd-CTG-VDUwl2jTW1JCUG0CAiaarMuEjeS9rXQg8PvmZc5B__oIbDpa-2bQVrfwHX8fYlnR2mKF3I5N0Nf4ZOUgLMWq8OJC0Hlo50uUxwjTmTAJfPu5dHf4l-HN91i3VY7HFiFBFUAyB-pcA4SiBTccFpcQbu1R9PmLlqFGH6-2TeelhH3uy87DypcbvKi1bgqfuAf-0HDOpZhtVOLE4mbipl9oE6VS3aiN-ypGk9dO0xIyYe4ksxw1TLSGh8-26Bt5EX6dy-2DRAdaUKs5dsd9BdyuObeOn75P-yaSMUVumJ5jo9p-OaYiYRbUcKA55R4lqSoNTTvTGMsCd6M-8WWEvGsABhvY8kuNnUCeffT=w530-h348-no)

### 訓練
訓練有兩種方式：
1. 「訓練」三連拍：用來「訓練」將來要進行辨識的人。

    python FacePI/FacePI.py Train <userData> <姓名>

2. 在「簽到」過程中，若發現無法辨認即可點擊 "a" 案件進行學習。


### 簽到
最後，進行簽到。

    python FacePI/FacePI.py Signin

即可依照畫面指示進行操作。
