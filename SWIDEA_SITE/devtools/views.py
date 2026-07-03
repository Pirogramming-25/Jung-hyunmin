# devtool/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import DevTool


def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'devtool/devtool_list.html', {'devtools': devtools})


def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    return render(request, 'devtool/devtool_detail.html', {'devtool': devtool})


def devtool_create(request):
    if request.method == 'POST':
        devtool = DevTool.objects.create(
            name=request.POST.get('name'),
            kind=request.POST.get('kind'),
            content=request.POST.get('content'),
        )
        return redirect('devtool-detail', pk=devtool.pk)
    return render(request, 'devtool/devtool_form.html')


def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        devtool.name = request.POST.get('name')
        devtool.kind = request.POST.get('kind')
        devtool.content = request.POST.get('content')
        devtool.save()
        return redirect('devtool-detail', pk=devtool.pk)
    return render(request, 'devtool/devtool_form.html', {'devtool': devtool})


def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        devtool.delete()
        return redirect('devtool-list')
    return render(request, 'devtool/devtool_detail.html', {'devtool': devtool})