from django.db.models import Case, IntegerField, When
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Idea, IdeaStar, DevTool
# Create your views here.

def idea_list(request):
  ideas = Idea.objects.all()
  sort = request.GET.get('sort', 'latest')
  if sort == 'name':
    ideas = ideas.order_by('title')
  elif sort == 'oldest':
    ideas = ideas.order_by('created_at')
  elif sort == 'star':
    ideas = ideas.annotate(
      has_star=Case(When(star__isnull=False, then=1), default=0, output_field=IntegerField())
    ).order_by('-has_star', '-created_at')
  elif sort == 'interest':
    ideas = ideas.order_by('-interest')
  else: #latest
    ideas = ideas.order_by('-created_at')

  return render(request, 'ideas/idea_list.html', {'ideas':ideas, 'sort':sort})

def idea_detail(request, pk):
  idea = get_object_or_404(Idea, pk=pk)
  return render(request, 'ideas/idea_detail.html', {'idea':idea})

def idea_create(request):
  if request.method == 'POST':
    idea = Idea.objects.create(
      title = request.POST.get('title'),
      content = request.POST.get('content'),
      interest = request.POST.get('interest'),
      devtool_id = request.POST.get('devtool'),
      image = request.FILES.get('image'),
    )
    return redirect('idea-detail', pk=idea.pk)
  devtools = DevTool.objects.all()
  return render(request, 'ideas/idea_form.html', {'devtools':devtools})

def idea_update(request, pk):
  idea = get_object_or_404(Idea, pk=pk)
  if request.method == 'POST':
    idea.title = request.POST.get('title')
    idea.content = request.POST.get('content')
    idea.interest = request.POST.get('interest')
    idea.devtool_id = request.POST.get('devtool')
    if request.FILES.get('image'):               # ← 새 이미지 있을 때만 교체
      idea.image = request.FILES.get('image')
    idea.save()
    return redirect('idea-detail', pk=idea.pk)
  devtools = DevTool.objects.all()
  return render(request, 'ideas/idea_form.html', {'idea':idea, 'devtools':devtools})

def idea_delete(request, pk):
  idea = get_object_or_404(Idea, pk=pk)
  if request.method == 'POST':
    idea.delete()
    return redirect('idea-list')
  return render(request, 'ideas/idea_delete.html', {'idea':idea})

@require_POST
def idea_star_toggle(request, pk):
  idea = get_object_or_404(Idea, pk=pk)
  try:
    idea.star.delete()
  except IdeaStar.DoesNotExist:
    IdeaStar.objects.create(idea=idea)
  next_url = request.POST.get('next') or 'idea-list'
  return redirect(next_url)

@require_POST
def idea_interest_update(request, pk):
  idea = get_object_or_404(Idea, pk=pk)
  action = request.POST.get('action')
  if action == 'increase':
    idea.interest += 1
  elif action == 'decrease':
    idea.interest = max(0, idea.interest - 1)
  idea.save(update_fields=['interest'])
  return JsonResponse({'interest': idea.interest})