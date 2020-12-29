from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from community.forms import *
from .models import Article


def home(request):
    return render(request, "community/home.html")


def write(request):
    # form tag 의 action 속성이 가리키는 페이지로 form 데이터가 전송됨.
    if request.method == 'POST':  # POST 형식 요청일 때
        form = Form(request.POST)
        if form.is_valid():  # 유효한 데이터라면
            form.save()  # form 을 그대로 DB에 저장
            return redirect('/community/list')
    else:
        form = Form()

    return render(request, 'community/write.html', {'form': form})  # {'"write.html"에서 사용할 변수이름': 넘겨줄 변수이름}



def list(request):
    articleList = Article.objects.all()  # models.py 의 Article 에서 만든 모든 DB column 을 가져온다
    return render(request, "community/list.html", {'articleList': articleList})


def view(request, article_id):
    # article = Article.objects.get(id=article_id)  # id와 일치하는 게시물 1개 가져옴.
    article = get_object_or_404(Article, id=article_id)  # 존재하지 않는 id를 요청할 때 404 페이지 출력
    return render(request, "community/view.html", {'article': article})


# 회원 가입
def signup(request):
    # signup 으로 POST 요청이 왔을 때, 새로운 유저를 만드는 절차를 밟는다.
    if request.method == 'POST':
        # password와 confirm에 입력된 값이 같다면
        if request.POST['password'] == request.POST['confirm']:
            # user 객체를 새로 생성
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            # 로그인 한다
            auth.login(request, user)
            return redirect('/community')
    # signup으로 GET 요청이 왔을 때, 회원가입 화면을 띄워준다.
    return render(request, 'community/signup.html')


# 로그인
def login(request):
    # login으로 POST 요청이 들어왔을 때, 로그인 절차를 밟는다.
    if request.method == 'POST':
        # login.html에서 넘어온 username과 password를 각 변수에 저장한다.
        username = request.POST['username']
        password = request.POST['password']

        # 해당 username과 password와 일치하는 user 객체를 가져온다.
        user = auth.authenticate(request, username=username, password=password)

        # 해당 user 객체가 존재한다면
        if user is not None:
            # 로그인 한다
            auth.login(request, user)
            return redirect('/community')
        # 존재하지 않는다면
        else:
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
            return render(request, 'community/login.html', {'error': 'username or password is incorrect.'})
    # login으로 GET 요청이 들어왔을때, 로그인 화면을 띄워준다.
    else:
        return render(request, 'community/login.html')


# 로그 아웃
def logout(request):
    # logout으로 POST 요청이 들어왔을 때, 로그아웃 절차를 밟는다.
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/community')

    # logout으로 GET 요청이 들어왔을 때, 로그인 화면을 띄워준다.
    return render(request, 'community/login.html')



