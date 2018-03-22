from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, render_to_response

from .forms import NetworkTestForm
from .zabbix import *
import urlparse

def _form_view(request, template_name='basic.html', form_class=NetworkTestForm):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            data = request.POST

            src = data['source']
            dst = data['destination']
            pro = data['protocol']
            port = data['port']

            check = zabbix_check(src, dst, pro, port)
            queryset = check.zabbix_get()
            context = {
                "queryset": queryset,
                "form" : form
            }
            return render(request, 'default.html', context)
    else:
        form = form_class()
    return render(request, template_name, {'form': form})

def default(request):
    return _form_view(request, template_name='default.html')
