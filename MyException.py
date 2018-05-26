import platform, ClassUtils

class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class responseError(Error):
    """Exception raised for errors when response error.
    """

    def __init__(self, message):
        self.message = message


class RateLimitExceededError(Error):
    ''' 專用於「達到存取上限」 '''
    def __init__(self, message):
        self.message = message
        print('「達到存取上限」, 稍等繼續。')


class PersonGroupNotFoundError(Error):
    ''' 「PersonGroup 不存在」，捕獲後必須自動建立預設 PersonGroup '''
    def __init__(self, message):
        self.message = message
        print('「PersonGroup 不存在」,將自動建立預設 PersonGroup')
    
class UnspecifiedError(Error):
    ''' 「驗證失敗」，API KEY 已經失效，請到 config 設定有效的 API KEY。 '''
    def __init__(self, message):
        self.message = message
        text = '「驗證失敗」，API KEY 已經失效，請到 config 設定有效的 API KEY。'
        print(text)
        if ClassUtils.isLinux():
            print(text)
        else:
            import ClassMessageBox
            ClassMessageBox.MessageGUI(message, text)

class esc_opencv(Error):
    ''' 「結束攝影鏡頭」 '''
    def __init__(self, message):
        self.message = message
        print('「結束攝影鏡頭」')
    