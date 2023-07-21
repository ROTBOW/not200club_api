from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Task, TaskThread

# Create your views here.

def ping(req) -> JsonResponse:
    return JsonResponse({'status': 'GOOD'})

@csrf_exempt
def dispatch_task(req) -> JsonResponse:
    res = dict()
    if req.method == 'GET':
        return JsonResponse({'log': 'This call does not support GET requests, to get finished data, or check if data is ready make a get request to ****'}, status=403)
    
    print(TaskThread.objects.all().count())
    
    
    if not res:
        res['status'] = 'idk'
    return JsonResponse(res)

def check_task(req, id) -> JsonResponse:
    '''
    Will check if task is finished, if not checks if there is a running task
    else returns the appropriate error.
    '''
    try:
        task = Task.objects.get(task_id=id)
    except Exception as e:
        task = None
    print(task)
    
    return JsonResponse({'item': id})