from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import Action

@login_required
def action_list(request):
    actions_list = Action.objects.all()
    paginator = Paginator(actions_list, 5)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)

    except EmptyPage:
        if request.is_ajax():
            return JsonResponse({'actions': ''})
        actions_list = paginator.page(paginator.num_pages)
    if request.is_ajax():
        data = {'actions': render_to_string('actions/action/detail.html', {'actions': actions_list})}
        return JsonResponse(data)
    return render(request, 'account/dashboard.html', 
                  {'section': 'actions',
                   'actions': actions_list})
