from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from django.views.generic import CreateView
import requests
import json


def home(request):
    return render(request, "community/home.html")


def index(request):
    articleList = Article.objects.all()  # models.py 의 Article 에서 만든 모든 DB column 을 가져온다
    return render(request, "community/index.html", {'articleList': articleList})


# 글 작성하는 generic view
class PostCreateView(CreateView):
    template_name = 'community/write.html'
    success_url = '/community/list'
    form_class = ArticleForm


def list(request):
    articleList = Article.objects.all()  # models.py 의 Article 에서 만든 모든 DB column 을 가져온다
    return render(request, "community/list.html", {'articleList': articleList})


def detail(request, article_id):
    # article = Article.objects.get(id=article_id)  # id와 일치하는 게시물 1개 가져옴.
    article = get_object_or_404(Article, pk=article_id)  # 존재하지 않는 게시물을 요청할 때 404 페이지 출력
    comments = Comment.objects.filter(article_id=article_id)  # 모델명.objects.filter() : select * where 절 역할

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            content = comment_form.cleaned_data['comment_textfield']  # clean_data[] 형태로 실제로 입력된 데이터에 해당되는 것을 받아옴

            print("댓글 :", content)

            # [카카오 로그인 API]
            # 1. 인가 코드 받기 - 우리가 설정한 redirect url 로 인가코드를 보냄.
            # 2. 인가 코드를 이용하여 Access Token 발급
            # 3. access_token 을 이용해 실제 카카오계정에서 사용중인 닉네임, 프로필사진을 가져옴.
            # 4. access_token 을 이용해 카카오톡 나에게 보내기 기능 사용.

            login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'

            client_id = 'REST API KEY'  # REST API 키. kakao developer 에서 알 수 있음. 자기만 알기.
            redirect_uri = 'http://127.0.0.1:8000/oauth'

            login_request_uri += 'client_id=' + client_id
            login_request_uri += '&redirect_uri=' + redirect_uri
            login_request_uri += '&response_type=code'
            login_request_uri += '&response_type=code&scope=talk_message'  # 동적동의에 필요

            # 세션변수 'client_id', 'redirect_uri' 에 담아서 oauth()로 보내기
            request.session['client_id'] = client_id
            request.session['redirect_uri'] = redirect_uri

            return redirect(login_request_uri)
        else:
            return redirect('/community/list')

    else:
        comment_form = CommentForm()

        context = {
            'article': article,
            'comments': comments,
            'comment_form': comment_form
        }

        return render(request, 'community/detail.html', context)


# detail 에서 http://127.0.0.1:8000/oauth 로 반환된 인가코드를 변수에 담아 출력 후 메인화면으로 전환
def oauth(request):
    code = request.GET['code']

    # 세션에서 받아오기
    client_id = request.session.get('client_id')
    redirect_uri = request.session.get('redirect_uri')

    # access token 생성
    access_token_request_uri = 'https://kauth.kakao.com/oauth/token?grant_type=authorization_code'
    access_token_request_uri += '&client_id=' + client_id
    access_token_request_uri += '&redirect_uri=' + redirect_uri
    access_token_request_uri += '&code=' + code

    # print(access_token_request_uri)

    # JSON 데이터 파싱
    access_token_request_uri_data = requests.get(access_token_request_uri)
    json_data = access_token_request_uri_data.json() # json() 함수를 통해 딕셔너리 형태로 변환
    access_token = json_data['access_token']  # 'access_token' key 의 value 를 가져온다
    print("access_token :", access_token)

    # access_token 을 이용해 실제 카카오계정에서 사용중인 닉네임, 프로필사진을 가져옴.
    user_profile_info_uri = "https://kapi.kakao.com/v1/api/talk/profile?access_token="
    user_profile_info_uri += str(access_token)

    user_profile_info_uri_data = requests.get(user_profile_info_uri)
    user_json_data = user_profile_info_uri_data.json()
    nickName = user_json_data['nickName']
    profileImageURL = user_json_data['profileImageURL']
    thumbnailURL = user_json_data['thumbnailURL']

    # print("nickName = " + str(nickName))
    # print("profileImageURL = " + str(profileImageURL))
    # print("thumbnailURL = " + str(thumbnailURL))

    # 카카오톡 나에게 보내기 예시 데이터
    template_dict_data = str({
        "object_type": "feed",
        "content": {
            "title": "디저트 사진",
            "description": "아메리카노, 빵, 케익",
            "image_url": "http://mud-kage.kakao.co.kr/dn/NTmhS/btqfEUdFAUf/FjKzkZsnoeE4o19klTOVI1/openlink_640x640s.jpg",
            "image_width": 640,
            "image_height": 640,
            "link": {
                "web_url": "http://www.daum.net",
                "mobile_web_url": "http://m.daum.net",
                "android_execution_params": "contentId=100",
                "ios_execution_params": "contentId=100"
            }
        },
        "social": {
            "like_count": 100,
            "comment_count": 200,
            "shared_count": 300,
            "view_count": 400,
            "subscriber_count": 500
        },
        "buttons": [
            {
                "title": "웹으로 이동",
                "link": {
                    "web_url": "http://www.daum.net",
                    "mobile_web_url": "http://m.daum.net"
                }
            },
            {
                "title": "앱으로 이동",
                "link": {
                    "android_execution_params": "contentId=100",
                    "ios_execution_params": "contentId=100"
                }
            }
        ]
    })

    kakao_to_me_uri = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",  # key-value and POST
        'Authorization': "Bearer " + access_token,
    }

    # json.dumps() : 딕셔너리를 JSON 형태로 변환
    # JSON 데이터는 키 값이 ''로 감싸고 있는 것이 아니라 ""로 감싸므로 치환.
    template_json_data = "template_object=" + str(json.dumps(template_dict_data))
    template_json_data = template_json_data.replace("\"", "")
    template_json_data = template_json_data.replace("'", "\"")

    # requests.request() 를 이용해 카카오톡 나에게 보내기
    requests.request(method="POST", url=kakao_to_me_uri, data=template_json_data, headers=headers)

    # response = requests.request(method="POST", url=kakao_to_me_uri, data=template_json_data, headers=headers)
    # print(response.json())  # {'result_code': 0} : 성공

    return redirect('/community')


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



# def write(request):
#     if request.method == 'POST':  # POST 형식 요청일 때
#         form = Form(request.POST)
#         if form.is_valid():  # 유효한 데이터라면
#             form.save()  # form 을 그대로 DB에 저장
#             return redirect('/community/list')
#     else:
#         form = Form()
#     return render(request, 'community/write.html', {'form': form})  # {'"write.html"에서 사용할 변수이름': 넘겨줄 변수이름}
