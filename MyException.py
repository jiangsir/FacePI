
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
    ''' 專用於「PersonGroup 不存在」，捕獲後必須自動建立預設 PersonGroup '''
    def __init__(self, message):
        self.message = message
        print('「PersonGroup 不存在」,將自動建立預設 PersonGroup')
    
class connectError():
    ''' 專用於「連線失敗」，呼叫 FaceAPI 失敗，通常是網路不通。 '''
    