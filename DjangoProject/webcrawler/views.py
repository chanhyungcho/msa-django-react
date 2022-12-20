from django.http import JsonResponse
from rest_framework.decorators import api_view

from webcrawler.services import ScrapService

@api_view(['GET'])
def crawler(request):
    if request.method == 'GET':
        return JsonResponse({'영화':
                ScrapService().naver_movie_review()})

    else:
        return JsonResponse({'result' : 'error'})

