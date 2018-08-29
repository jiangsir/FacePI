from django.shortcuts import render
from FacePIapp import ClassDB
import base64, os, json

# Create your views here.


def facepiapp_view(request):
    basepath = os.path.dirname(os.path.realpath(__file__))
    configpath = os.path.join(basepath, '../../Config.json')
    with open(configpath, 'r', encoding='utf-8') as f:
        config = json.load(f)

    signins = ClassDB.BaseDB.query("SELECT * FROM signins WHERE apikey='" +
                                   config['api_key'] + "' AND groupid='" + config['personGroupId'] + "' ORDER BY id DESC", None)

    for signin in signins:
        #signin['faceimage_base64'] = base64.b64encode(signin['faceimage'])
        signin['faceimage_base64'] = base64.b64encode(
            signin['faceimage']).decode()

    persons = [{'name': 'tom'}, {'name': 'mary'}, {'name': 'jiang'}]
    context = {'data': 'hello django!!!',
               'persons': persons, 'signins': signins}
    return render(request, 'FacePIapp.html', context)
