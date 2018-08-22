from django.shortcuts import render
from FacePIapp import ClassDB
import base64

# Create your views here.
def facepiapp_view(request):
    signins = ClassDB.BaseDB.query('SELECT * FROM signins ORDER BY id DESC', None)

    for signin in signins:
        #signin['faceimage_base64'] = base64.b64encode(signin['faceimage'])
        signin['faceimage_base64'] = base64.b64encode(signin['faceimage']).decode()

    persons = [{'name': 'tom'}, {'name': 'mary'}, {'name': 'jiang'}]
    context = {'data': 'hello django!!!', 'persons': persons, 'signins': signins }
    return render(request, 'FacePIapp.html', context)

