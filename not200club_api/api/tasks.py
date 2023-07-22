import threading

import requests

from .models import Task

def get_worker_count() -> int:
    return threading.active_count()

def worker_data() -> dict:
    res = {
        'workers_active': 0,
        'workers': [],
    }
    
    for worker in threading.enumerate():
        res['workers'].append(worker.name)
        res['workers_active'] += 1
        
    return res

def send_worker() -> None:
    if Task.objects.filter(task_finished=False, task_reserved=False).count() == 0:
        return 
    
    task = Task.objects.filter(task_finished=False, task_reserved=False).earliest('timestamp')
    create_thread_worker(task.task_id, task.task_url)

def check_url_update_task(task_id: str, url: str) -> None:
    print(f'* Created {task_id} Task!')
    t = Task.objects.get(task_id=task_id)
    t.task_reserved = True
    t.save()
    
    try:
        r = requests.get(url, timeout=120)
        t.time_to_respond = r.elapsed
        t.status_code = str(r.status_code)
    except requests.exceptions.Timeout:
        t.timeout_res = True
    except:
        t.bad_url = True
    
    
    t.task_finished = True
    t.save()
    print(f' * {task_id} Task Complete!')
    
    if len(list(threading.enumerate())) <= 21:
        send_worker()

def create_thread_worker(task_id, task_url) -> None:
    t = threading.Thread(target=check_url_update_task, args=(task_id, task_url), name=task_id)
    t.start()