import os
import subprocess


def os_exec(cmd):
    print('run_cmd=', cmd)
    try:
        completed = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as err:
        print('ERROR:', err)
    else:
        print('returncode:', completed.returncode)
        print('STDOUT: {!r}'.format(len(completed.stdout)),
              completed.stdout.decode('utf-8'))
        print('STDERR: {!r}'.format(len(completed.stderr)),
              completed.stderr.decode('utf-8'))

# %ALLUSERSPROFILE%
# %HomeDrive%%HomePath%
print('USERPROFILE=', os.environ['USERPROFILE'])
print('ALLUSERSPROFILE=', os.environ['ALLUSERSPROFILE'])
print('HOME=', os.environ['HomeDrive']+os.environ['HomePath'])
ALLUSERSPROFILE = os.environ['ALLUSERSPROFILE']

os_exec('python --version')
os_exec('python -m pip install --upgrade pip')

#os.system('conda install -c menpo opencv3 -y')
os_exec('pip install opencv-python==3.1.0')
# pip install opencv-python==3.1.0  若用 pip 要指定安裝 opencv 3.1.0
os_exec('pip install cython msgpack fire Pillow pypinyin django pymysql scipy scikit-image cmake imutils')
os_exec('pip install dlib==18.17.100')
