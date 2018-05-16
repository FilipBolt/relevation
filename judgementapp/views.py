# Create your views here.
from collections import defaultdict
import cStringIO as StringIO
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from judgementapp.models import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User


@login_required
def index(request):
    return render_to_response('judgementapp/index.html', context_instance=RequestContext(request))


@login_required
@permission_required('judgementapp.can_upload_docs')
def qrels(request):
    judgements = Judgement.objects.exclude(relevance=-1)

    response = HttpResponse(judgements, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=qrels.txt'
    #response['X-Sendfile'] = myfile
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response


@login_required
def query_list(request):
    annotator = User.objects.get(username=request.user)
    queries = Query.objects.filter(annotator=annotator).order_by('qId')
    return render_to_response(
        'judgementapp/query_list.html', 
        {'queries': queries}, 
        context_instance=RequestContext(request)
    )


@login_required
def query(request, qId):
    userAnnotator=User.objects.get(username=request.user)
    query = Query.objects.get(qId=qId, annotator=userAnnotator)
    judgements = Judgement.objects.filter(query=query.id, annotator=userAnnotator)

    if "difficulty" in request.POST:
        query.difficulty = int(request.POST['difficulty'])
        if "comment" in request.POST:
            query.comment = request.POST['comment']
        query.save()

    query.length = len(query.text)

    return render_to_response('judgementapp/query.html', {'query': query, 'judgements': judgements},
                              context_instance=RequestContext(request))


@login_required
def document(request, qId, docId):
    userAnnotator = User.objects.get(username=request.user)
    document = Document.objects.get(docId=docId)
    query = Query.objects.get(qId=qId, annotator=userAnnotator)

    judgements = Judgement.objects.filter(query=query.id, annotator=userAnnotator)
    judgement = Judgement.objects.filter(
        query=query.id, document=document.id, annotator=userAnnotator)[0]
    rank = -1
    for (count, j) in enumerate(judgements):
        if j.id == judgement.id:
            rank = count + 1
            break

    prev = None
    try:
        prev = Judgement.objects.filter(query=query.id, annotator=userAnnotator).get(id=judgement.id-1)
    except:
        pass

    next = None
    try:
        next = Judgement.objects.filter(query=query.id, annotator=userAnnotator).get(id=judgement.id+1)
    except:
        pass

    content = document.get_content()
    title = document.get_title()
    return render_to_response(
        'judgementapp/document.html',
        {'document': document,
         'query': query, 'judgement': judgement,
         'next': next, 'prev': prev, 'rank': rank,
         'total_rank': judgements.count(),
         'content': content.strip(),
         'title': title 
        }, context_instance=RequestContext(request)
    )

@login_required
def judge(request, qId, docId):
    userAnnotator = User.objects.get(username=request.user)
    query = get_object_or_404(Query, qId=qId, annotator=userAnnotator)
    document = get_object_or_404(Document, docId=docId)
    relevance = request.POST['relevance']
    comment = request.POST['comment']

    judgements = Judgement.objects.filter(query=query.id, annotator=userAnnotator)
    judgement, created = Judgement.objects.get_or_create(
        query=query.id, document=document.id, annotator=userAnnotator)

    judgement.relevance = int(relevance)
    if comment != 'Comment':
        judgement.comment = comment

    judgement.annotator = request.user
    judgement.save()

    next = None
    try:
        next = Judgement.objects.filter(
            query=query.id, annotator=userAnnotator).get(id=judgement.id+1)
        if 'next' in request.POST:
            document = next.document
            judgement = next
            next = Judgement.objects.filter(
                query=query.id, annotator=userAnnotator).get(id=judgement.id+1)
    except:
        pass

    prev = None
    try:
        prev = Judgement.objects.filter(
            query=query.id, annotator=userAnnotator).get(id=judgement.id-1)
    except:
        pass

    rank = -1
    for (count, j) in enumerate(judgements):
        if j.id == judgement.id:
            rank = count+1
            break

    content = document.get_content()

    return render_to_response('judgementapp/document.html', {
        'document': document, 'query': query, 'judgement': judgement,
        'next': next, 'prev': prev, 'rank': rank, 
        'total_rank': judgements.count(), 
        'content': content.strip()
    }, context_instance=RequestContext(request))


@login_required
@permission_required('judgementapp.can_upload_docs')
def upload(request):
    context = {}
    if 'queryFile' in request.FILES:
        f = request.FILES['queryFile']

        qryCountPerUser = defaultdict(int)
        for query in f:
            qid, user, txt = query.split(",", 2)
            # checking if user exists
            userAnnotator = User.objects.get(username=user)
            qryCountPerUser[user] += 1
            query = Query(qId=qid, text=txt)
            query.annotator = userAnnotator
            query.save()
        context['queries'] = dict(qryCountPerUser)

    if 'resultsFile' in request.FILES:
        f = request.FILES['resultsFile']

        docCountPerUser = defaultdict(int)
        for result in f:
            qid, doc, user = result.split(',')
            doc = doc.replace('corpus/', '')
            user = user.strip()
            docCountPerUser[user] += 1

            document, created = Document.objects.get_or_create(docId=doc)
            document.text = "TBA"
            userAnnotator = User.objects.get(username=user)
            query = Query.objects.get(qId=qid, annotator=userAnnotator)
            document.save()

            judgement = Judgement()
            judgement.query = query
            judgement.document = document
            # check user exists in the DB
            # if not this, will throw an exception
            userAnnotator = User.objects.get(username=user)
            judgement.annotator = userAnnotator
            judgement.relevance = -1

            judgement.save()

        context['results'] = dict(docCountPerUser)

    return render_to_response('judgementapp/upload.html', context, context_instance=RequestContext(request))


def login_user(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    context['form'] = form
    return render_to_response('judgementapp/login.html', context)
