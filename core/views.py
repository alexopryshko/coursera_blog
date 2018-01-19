from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render

from core.models import Topic, Category


def index(request):
    topics = Topic.objects.all().annotate(Count('categories'))
    categories = Category.objects.all()

    q = request.GET.get('q')
    if q is not None:
        topics = topics.filter(title__icontains=q)
    category_pk = request.GET.get('category')
    if category_pk is not None:
        topics = topics.filter(categories__pk=category_pk)

    return render(request, 'core/index.html', context={
        'topics': topics,
        'categories': categories
    })


def topic_details(request, pk):
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        raise Http404
    return render(request, 'core/topic_details.html', context={
        'topic': topic
    })
