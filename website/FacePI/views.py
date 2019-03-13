from django.shortcuts import render

# Create your views here.


def facepi_view(request):
    context = {}
    return render(request, 'FacePI.html', context)
