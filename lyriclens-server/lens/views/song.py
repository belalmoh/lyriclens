from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@require_http_methods(["GET"])
@csrf_exempt
def get_song_summary(request):
    return JsonResponse({"message": "Hello, world!"})