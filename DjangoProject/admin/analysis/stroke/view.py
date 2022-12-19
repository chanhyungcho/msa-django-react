from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from admin.analysis.stroke.model import StrokeModel


@api_view(['GET'])
def stroke(request):
    StrokeModel().hook()
    print(f'Enter Stroke with {request}')
    return JsonResponse({'Response Test':'SUCCESS'})
