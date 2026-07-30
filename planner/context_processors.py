from .models import ChecklistItem
from collections import defaultdict
from django.utils.timezone import localdate


# def checklist_items_processor(request):
#     return {
#         'checklist_items': ChecklistItem.objects.order_by('completed', 'id')
#     }


def checklist_context(request):
    pending = defaultdict(list)
    done = defaultdict(list)

    for i in ChecklistItem.objects.all().order_by('-created_at'):
        day = localdate(i.created_at)
        (done if i.completed else pending)[day].append(i)

    return {
        'pending_grouped': dict(pending),
        'done_grouped': dict(done),
    }

