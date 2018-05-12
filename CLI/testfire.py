import os,fire
# pip install fire

class Calculator:
  ''' 計算機 '''
  def __init__(self):
    pass

  def __privateMethod(self):
    ''' sssss ''' 
    print('private Call')
    return -1

  def add(self, x, y):
    ''' 加法 '''
    self.__privateMethod()
    return x + y

  def multiply(self, x, y):
    ''' 減法 '''
    return x * y

if __name__ == '__main__':
  fire.Fire(Calculator)

#if __name__ == '__main__':
#    fire.Fire()
