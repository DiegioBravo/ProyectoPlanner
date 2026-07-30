from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Day, HourSlot, Task, TaskAttachment, SubChecklistItem
from .forms import TaskForm
from .forms import TaskAttachmentForm
from datetime import datetime, time, timedelta
from django.urls import reverse
from datetime import date
from .models import ChecklistItem
from django.http import JsonResponse
from django.utils.timezone import localtime, localdate
from django.utils.formats import date_format
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import json


# Rango de horas por defecto (ajusta si deseas)
START_HOUR = 7
END_HOUR = 19  # no inclusivo, crea slots hasta 18:00-19:00


@login_required
@require_POST
def delete_subtask(request, pk):
    SubChecklistItem.objects.filter(pk=pk,checklist__user=request.user).delete()
    return JsonResponse({'ok': True})


@login_required
@require_POST
def toggle_subtask(request, pk):
    sub = get_object_or_404(SubChecklistItem,pk=pk,checklist__user=request.user)
    sub.completed = not sub.completed
    sub.save()
    return JsonResponse({'ok': True})


@login_required
def add_subtask(request):

    if request.method == 'POST':

        checklist_id = request.POST.get('checklist_id')
        text = request.POST.get('text')

        # Validar que el checklist pertenezca al usuario
        checklist = get_object_or_404(
            ChecklistItem,
            pk=checklist_id,
            user=request.user
        )

        # Crear subtarea
        sub = SubChecklistItem.objects.create(
            checklist=checklist,
            text=text
        )

        return JsonResponse({
            'id': sub.id,
            'text': sub.text,
            'completed': sub.completed
        })
    

@login_required
def subtasks_list(request, checklist_id):
    subtasks = SubChecklistItem.objects.filter(
    checklist_id=checklist_id,
    #checklist__user=request.user
    ).order_by('created_at')

    data = [{
    'id': s.id,
    'text': s.text,
    'completed': s.completed
    } for s in subtasks]


    return JsonResponse(data, safe=False)


@login_required
@require_POST
def actualizar_urgencia_checklist(request, pk):

    if request.method == 'POST':
        data = json.loads(request.body)
        item = get_object_or_404(ChecklistItem,pk=pk,user=request.user)
        item.urgencia = int(data['urgencia'])
        item.save()

        return JsonResponse({'ok': True})


@login_required
def today_redirect(request):
    today = date.today().strftime("%Y-%m-%d")
    return redirect('planner:day_view', date_str=today)


@login_required
def index(request):

    fecha = date.today().strftime("%Y-%m-%d")

    days = Day.objects.filter(
        user=request.user
    ).order_by('-date')

    User = get_user_model()

    usuarios = User.objects.all().order_by('username')

    return render(request, 'planner/index.html', {

        'fecha': fecha,
        'days': days,
        'usuarios': usuarios

    })


def create_day_if_not_exists(user, date_obj):

    day, created = Day.objects.get_or_create(
        user=user,
        date=date_obj
    )

    if created:
        for h in range(START_HOUR, END_HOUR):
            start = time(h, 0)
            end = (
                datetime.combine(date_obj, start)
                + timedelta(hours=1)
            ).time()
            HourSlot.objects.create(
                day=day,
                start_time=start,
                end_time=end
            )
    return day


@login_required
def day_view(request, date_str=None):
    # si no se pasa fecha, usar hoy
    if date_str:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date_obj = datetime.today().date()
    day = create_day_if_not_exists(request.user,date_obj)
    hours = day.hours.all()  # gracias a ordering en HourSlot
    return render(request, 'planner/day_view.html', {'day': day, 'hours': hours})


@login_required
def add_task(request, hourslot_id):
    hourslot = get_object_or_404(HourSlot,pk=hourslot_id,day__user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.hourslot = hourslot
            task.save()
            return redirect(reverse('planner:day_view', args=[hourslot.day.date.isoformat()]))
    else:
        form = TaskForm()
    return render(request, 'planner/task_form.html', {'form': form, 'hourslot': hourslot})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task,pk=task_id,hourslot__day__user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse('planner:day_view', args=[task.hourslot.day.date.isoformat()]))
    else:
        form = TaskForm(instance=task)
    return render(request, 'planner/task_form.html', {'form': form, 'task': task, 'hourslot': task.hourslot})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task,pk=task_id,hourslot__day__user=request.user)
    day = task.hourslot.day

    if task.attachments.exists():
        messages.error(
            request,
            "No puedes eliminar esta tarea porque tiene archivos adjuntos."
        )
        return redirect(
            reverse('planner:day_view', args=[day.date.isoformat()])
        )

    if request.method == 'POST':
        task.delete()
        messages.success(request, "Tarea eliminada correctamente.")
        return redirect(
            reverse('planner:day_view', args=[day.date.isoformat()])
        )

    return render(request, 'planner/confirm_delete.html', {'task': task})


@login_required
def add_attachment(request, task_id):
    task = get_object_or_404(Task,pk=task_id,hourslot__day__user=request.user)

    if request.method == 'POST':
        form = TaskAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.task = task
            attachment.save()

    return redirect(
        'planner:day_view',
        date_str=task.hourslot.day.date.strftime('%Y-%m-%d')
    )


@login_required
@require_POST
def delete_attachment(request, attachment_id):
    attachment = get_object_or_404(TaskAttachment,pk=attachment_id,task__hourslot__day__user=request.user)

    # Guardamos el día antes de borrar
    day_date = attachment.task.hourslot.day.date

    # Borra archivo físico y registro
    attachment.file.delete(save=False)
    attachment.delete()

    return redirect('planner:day_view', day_date.isoformat())
    

@login_required
def add_checklist_item(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        item = ChecklistItem.objects.create(user=request.user,text=text)

        day = localdate(item.created_at)

        label = date_format(day, "l d M Y")
        label = label.capitalize()

        return JsonResponse({
            'id': item.id,
            'text': item.text,
            'day': day.isoformat(),
            'day_label': label,
        })


@login_required
@require_POST
def toggle_checklist(request, item_id):
    item = get_object_or_404(ChecklistItem,pk=item_id,user=request.user)
    item.completed = not item.completed
    item.save()
    return JsonResponse({'completed': item.completed})


@login_required
@require_POST
def delete_checklist(request, item_id):
    item = get_object_or_404(ChecklistItem,pk=item_id,user=request.user)
    item.delete()
    return JsonResponse({'deleted': True})


@login_required
def edit_subtask(request, subtask_id):
    if request.method == 'POST':
        subtask = get_object_or_404(SubChecklistItem,id=subtask_id,checklist__user=request.user)
        subtask.text = request.POST.get('text')
        subtask.save()
        return JsonResponse({
            'success': True
        })

