# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from UserManage.models import *
# Requests for Buzz API
import requests

def main_page(request):
  return render_to_response('main.html')

def logout_user(request):
  logout(request)
  return HttpResponseRedirect('/user/')

@csrf_exempt
def register_user(request):
  state = ''
  if request.POST:
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    if password1 == '':
      state = '패스워드를 입력하셔야 합니다'
      return render_to_response('registerform.html', {'state':state})
    if password1 != password2:
      state = '패스워드가 다릅니다'
      return render_to_response('registerform.html', {'state':state})
    try:
      find = User.objects.get(username=username)
    # 없으면 생성
    except User.DoesNotExist:
      user = User.objects.create_user(username=username, password=password1)
      user.save()
      state = '등록이 완료되었습니다. 로그인해주세요.'
      return render_to_response('registerform.html',{'state':state,})
    # 중복되면 문제
    else:
      state = '이미 가입된 아이디입니다.'
      return render_to_response('registerform.html', {'state':state})
  return render_to_response('registerform.html', {'state':state})

def search_request(variable, page, count):
    web_addr = 'http://17.buzzni.com:91/search/metaSearch?'
    web_addr += ('query=' + str(variable))
    web_addr += ('&page=' + str(page))
    web_addr += ('&num =' + str(count))
    search_result = requests.get(web_addr)
    jsonned = search_result.json()
    data = jsonned['result']['data']
    return data

@csrf_exempt
def user_page(request):
  state = ''
  # post면 로그인
  if request.POST:
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        state = '로그인됨'
        login(request, user)
        return render_to_response('loggedon.html',{'state':state, 'user':request.user})
      else:
        state = "your account is not active"
        return render_to_response('loggedon.html',{'state':state})
    else:
      state = "your id and/or password are incorrect"
      return render_to_response('loggedon.html',{'state':state})

  # get이면 쿼리 저장
  content = ''
  current = ''
  searchBox = ''
  if request.GET:
    # if username exists,  
    if request.user is not None:
      username = request.user.username
    if username == 'sogo':
      username = 'unknown_loggedonMode'
    # do requests
    content = request.GET.get('content')
    current = request.GET.get('current')
    searchBox = request.GET.get('searchBox')
    if searchBox == u'prev':
        if int(current) is not 1:
            current -= 1
    elif searchBox == u'next':
        if int(current) is not 1:
            current += 1
    result = search_request(content.encode('utf-8'), current, 10)
    # requests over
    if not content:
      state = 'please type anything'
      return render_to_response('loggedon.html',{'state':state})
    else:
      # 본격적인 모듈, 쿼리를 저장하고 점수를 받아낸다
      query = querySet(username=username, content=content)
      query.save()
      #state = 'query saved!'
      return render_to_response('loggedon.html',{'state':state,'result':result, 'content':content, 'current':current})
  return render_to_response('loggedon.html')

def get_query(request):
  username = 'unknown'
  content = ''
  current = ''
  searchBox = ''
  state = ''
  if request.GET:
    content = request.GET.get('content')
    current = request.GET.get('current')
    searchBox = request.GET.get('searchBox')
    if searchBox == u'prev':
        if int(current) is not 1:
            current -= 1
    elif searchBox == u'next':
        if int(current) is not 1:
            current += 1
    if not content:
      state = 'please type anything'
      return render_to_response('loggedon.html',{'state':state})
    else:
      # do requests
      result = search_request(content.encode('utf-8'), current, 10)
      query = querySet(username=username, content=content)
      query.save()
      state = 'query saved!'
      return render_to_response('noUserQuery.html',{'state':state,'result':result, 'content':content, 'current':current})
  return render_to_response('noUserQuery.html')
