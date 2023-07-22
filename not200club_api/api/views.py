from hashlib import sha256

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Task
from .tasks import get_worker_count, create_thread_worker, worker_data
from .utls import validate_url

# Create your views here.

def ping(req) -> JsonResponse:
    return JsonResponse({'status': 'GOOD'})

def check_workers(req) -> JsonResponse:
    return JsonResponse(worker_data())

@csrf_exempt
def dispatch_task(req) -> JsonResponse:
    if req.method == 'GET':
        return JsonResponse({'log': 'This call does not support GET requests, to get finished data, or check if data is ready make a get request to api/check_task/<task_id>'}, status=403)
    
    if sha256(req.POST['password'].encode('utf-8')).hexdigest() != '718723ed836bf94ccec7d66c40995dc19e1b4fe211518c3ad3b6aa570765c473':
        return JsonResponse({"task": 'Not allowed - BAD PASSWORD'}, status=401)
    
    if Task.objects.filter(task_id=req.POST['id']).exists():
        Task.objects.get(task_id=req.POST['id']).delete()
        
    new_task = Task()
    new_task.task_id = req.POST['id']
    new_task.task_url = validate_url(req.POST['url'])
    new_task.save()
    
    if get_worker_count() <= 20:
        create_thread_worker(req.POST['id'], validate_url(req.POST['url']))
    
    return JsonResponse({'task': 'task successfully create'})

def check_task(req, id) -> JsonResponse:
    '''
    Will check if task is finished, if not checks if there is a running task
    else returns the appropriate error.
    '''
    
    try:
        task = Task.objects.get(task_id=id)
    except Exception as e:
        return JsonResponse({'task': 'task does not exist'}, status=404)
    
    if not task.task_finished:
        # check if free worker
        return JsonResponse({'task': 'task has not finished yet'})
    
    res = {
            'task_id': task.task_id,
            'task_url': task.task_url,
            'status_code': task.status_code,
            'bad_url': task.bad_url,
            'time': task.time_to_respond,
            'timeout': task.timeout_res
        }
    
    
    return JsonResponse(res)