import json
import secrets
import smtplib
import ssl
import string
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
from sys import platform

from django.db.models import Sum, F, Q
from rest_framework.templatetags.rest_framework import data

from exhibition.models import Exhibition
from notification.models import Notification
from school.models import School
from visitRecord.models import VisitRecord

ssl._create_default_https_context = ssl._create_unverified_context

from allauth.socialaccount.models import SocialAccount
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import Member, MemberFile
from member.serializers import MemberSerializer
from oneLabProject import settings
from university.models import University




class MemberCheckIdView(APIView):
    def get(self, request):
        member_id = request.GET['member-id']
        is_duplicated = Member.objects.filter(member_id=member_id).exists()
        return Response({'isDup': is_duplicated})


class MemberNormalJoinView(View):
    def get(self, request):
        context = {
            'memberEmail': request.GET.get('member_email'),
            'memberSchoolEmail': request.GET.get('member_school_email'),
            'id': request.GET.get('id')
        }

        return render(request, 'login/normal-student-join.html', context)

    @transaction.atomic
    def post(self, request):
        data = request.POST
        university_major = data['university-member-major']
        data = {
            'member_name': data['member-name'],
            'member_password': data['member-password'],
            'member_email': data['member-email'],
            'member_school_email': data['member-school-email'],
            'member_phone': data['member-phone'],

        }

        member = Member.objects.create(**data)

        # member = Member.objects.filter(id=request.POST.get('id'))
        # # OAuth 최초 로그인 후 회원가입 시
        # if member.exists():
        #     del data['member_email']
        #     data['updated_date'] = timezone.now()
        #     member.update(**data)
        #
        # else:
        #     member = Member.objects.create(**data)
        member = Member.objects.get(id=member.id)
        university_info = {
            'university_member_birth': "1999-09-22",
            'university_member_major': university_major,
            'member': member
        }
        print(university_info)

        University.objects.create(**university_info)

        return redirect('member:login')


class MemberJoinView(View):
    def get(self, request):
        print(request.GET.get('member_name'))
        context = {
            'memberEmail': request.GET.get('member_email'),
            'memberType': request.GET.get('member_type'),
            'memberName': request.GET.get('member_name'),
            'memberPhone': request.GET.get('member_phone'),
            'memberSchoolEmail': request.GET.get('member_school_email')
        }
        # member_info = request.session['join-member-data']
        # context = {
        #     'member_email': member_info['member_email'],
        #     'member_name': member_info['member_name']
        # }

        return render(request, 'login/college-student-join.html', context)

    @transaction.atomic
    def post(self, request):
        data = request.POST
        user = SocialAccount.objects.get(user=request.user)
        university_major = data['university-member-major']
        data = {
            # 'member_name': data['member-name'],
            'member_phone': data['member-phone'],
            # 'member_password': data['member-password'],
            # 'member_email': data['member-email'],
            'member_school_email': data['member-school-email'],
        }
        last_member = Member.objects.latest('id')

        # OAuth 검사
        # OAuth 최초 로그인 시 TBL_MEMBER에 INSERT된 회원 ID가 member_id 이다.
        member = Member.objects.filter(id=last_member.id, member_type__in=['naver','kakao','google'])
        #   1. 아이디는 중복이 없다
        #   2. 이메일과 타입에 중복이 있다.
        #   3. OAuth로 최초 로그인된 회원을 찾아라

        # OAuth 최초 로그인 후 회원 가입
        if member.exists():
            print("존재함")
            # del data['member_email']
            # data['updated_date'] = timezone.now()
            member.update(**data)

        else:
            print("존재함1")
            member = Member.objects.create(**data)

        member = Member.objects.get(id=last_member.id)
        university_info = {
            'university_member_birth': "1999-09-22",
            'university_member_major': university_major,
            'member': member
        }
        print(university_info, member.__dict__)

        University.objects.create(**university_info)

        return redirect('member:login')


class MemberLoginView(View):
    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request):
        data = request.POST
        data = {
            'member_email': data['member-email'],
            'member_password': data['member-password']
        }

        member = Member.objects.filter(member_email=data['member_email'], member_password=data['member_password'])
        # print(member)
        url = '/'
        if member.exists():
            # 성공
            request.session['member'] = MemberSerializer(member.first()).data
            url = '/'
            return redirect('/')

        return render(request, 'login/login.html', {'check': False})


class SendVerificationCodeView(APIView):
    def post(self, request, school):
        data = request.POST
        # data = {
        #     # 'member_email': data['member-email'],
        #     'member_school_email': data['member-school-email'],
        # }
        # print(data['member-school-email'])
        # mail_receiver = data.get('member_school_email')
        # mail_receiver = json.dump(data)
        mail_receiver = school
        print(mail_receiver)
        rn = ''.join(random.choices('0123456789', k=6))


        port = 587
        smtp_server = "smtp.gmail.com"
        sender_email = "wmoon0024@gmail.com"
        receiver_email = mail_receiver
        password = "pqxh ciic adcg numz"
        message = f"<h1>인증번호 6자리 입니다 : {rn}</h1>"

        print("메일 들어옴")
        msg = MIMEText(message, 'html')
        data = MIMEMultipart()
        data.attach(msg)

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            print("들어옴1")
            server.starttls(context=context)
            print("들어옴2")
            server.ehlo()
            print("들어옴3")
            server.login(sender_email, password)
            print("들어옴4")
            server.sendmail(sender_email, receiver_email, data.as_string())
            # print("들어옴5")
            # server.quit()
        # server.sendmail(sender_email, receiver_email, data.as_string())
        # uri = request.get_full_path()
        # request.session['previous_uri'] = uri
        # previous_page = request.META.get('HTTP_REFERER')
        # return render(previous_page)
        # return JsonResponse({'success': True, 'message': '성공!!!'})

class MemberIdSearchView(View):
    def get(self, request):
        return render(request, 'login/account-find.html')

class MemberActivateEmailView(APIView):
    def get(self,request):
        pass

    def post(self, request, email):
        # data = request.POST
        # data = {
        #     'member_email': data['member_email']
        # }

        members = Member.objects.all()
        member_email = Member.objects.get(member_email=email)
        member_id = member_email.id
        print(member_id)
        print("id 들어옴")
        # print(member_id)


        # 랜덤 숫자랑 문자열 10자리
        # 이메일 링크를 받으면 적어도 그 링크를 통해 접속이 된다.
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        # 세션에 랜덤 코드 추가
        request.session['random_code'] = code
        # # 세션 저장
        # request.session.save()

        print(request.session['random_code'])

        # if member_email.exists():

        print(email)
        print(request.POST)
        # print(data['member-school-email'])
        mail_receiver = email
        # mail_receiver = json.dump(data)
        # mail_receiver = 'wmoon0024@gmail.com'
        print(mail_receiver)

        port = 587
        smtp_server = "smtp.gmail.com"
        sender_email = "wmoon0024@gmail.com"
        receiver_email = mail_receiver
        password = "pqxh ciic adcg numz"
        message = (f"<h1>비밀번호 계정 링크 입니다.</h1>\n"
                   f"<h2>http://127.0.0.1:10000/member/account-reset/{member_id}/{code}</h2>")

        print("메일 들어옴")
        msg = MIMEText(message, 'html')
        data = MIMEMultipart()
        data.attach(msg)

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            print("들어옴1")
            server.starttls(context=context)
            print("들어옴2")
            server.ehlo()
            print("들어옴3")
            server.login(sender_email, password)
            print("들어옴4")
            server.sendmail(sender_email, receiver_email, data.as_string())

            return Response('fasjfksa')


class MemberResetPasswordView(View):
    def get(self, request, id, random):
        del request.session['random_code']
        print("아이디", id)
        print("랜덤", random)


        member = Member.objects.get(id=id)
        print("아이디13들어옴")
        print(member.id)

        data = {
            'id': member.id,
            'random': random
        }
        print("여기까지 들어옴")

        # if member.id == id:
        #     member.save(update_fields=['member_password'])
        # 수정된 정보가 있을 수 있기 때문에 세션 정보 최신화
        # request.session['member'] = MemberSerializer(Member.objects.get(id=request.session['member']['id'])).data
        # check = request.GET.get('check')
        # context = {'check': check}
        return render(request, 'login/reset-link.html', data)

    def post(self, request, id, random):
        print("패스워드쪽 들어옴")
        data = request.POST
        data = {

            'member_id': data['member-id'],
            'member_password': data['member-password'],
        }
        print("패스워드 들어옴1")

        member = Member.objects.get(id=id)
        member.member_password = data['member_password']
        print("패스워드 들어옴2")

        member.save(update_fields=['member_password'])
        print("패스워드 들어옴3")
        return render(request, 'login/login.html')


class MemberMainView(View):
    def get(self, request):
        # member_name = request.session.get('member_name')
        request.session['member_name'] = MemberSerializer(Member.objects.get(id=request.session['member']['id'])).data
        print(request.session['member_name'])
        member = request.session['member']['id']
        profile = MemberFile.objects.filter(member_id=member).first()

        default_profile_url = 'https://static.wadiz.kr/assets/icon/profile-icon-1.png'

        if profile is None :
            profile = default_profile_url
            context = {
                'profile' : profile
            }
            return render(request, 'main/main-page.html', context)
        else :
            context = {
                'profile': profile
            }

            return render(request, 'main/main-page.html',context)


# 관리자 로그인 View
class AdminMemberLoginView(View):
    def get(self, request):
        # 관리자 로그인 페이지로 이동
        return render(request, 'admin/login.html')

    def post(self, request):
        # POST 메소드로 데이터를 받아옴.
        data = request.POST
        # 받아온 데이터를 다시 구성
        data = {
            'member_email': data['member-email'],
            'member_password': data['member-password'],
        }

        # exists() 를 사용하기 위해서 QuerySet 객체로 조회
        # first()를 사용하여 첫 번째 멤버 객체를 가져옴.
        member = Member.objects.filter(**data).first()
        url = 'member:admin_login'
        if member and member.member_status == False:
            # 로그인 성공
            request.session['member'] = MemberSerializer(member).data
            return redirect('member:admin_main')
        # 로그인 실패시 이동할 url
        return redirect(url)

# 관리자 메인 View
class AdminMainView(View):
    def get(self, request):
        # 오늘 날짜를 XXXX-XX-XX 의 형태로 저장
        today = timezone.now().date()
        # 일주일간 날짜 표기를 위해 오늘로부터 6을 빼줌.
        seven_days_ago = today - timedelta(days=6)
        # VisitRecord중, date__range를 통해 7일간의 방문자수를 가져온다.
        visit_records = VisitRecord.objects.filter(date__range=[seven_days_ago, today])
        # VisitRecord중, date=today로 오늘 방문자수를 가져온다.
        today_records = VisitRecord.objects.get(date = today)
        # 방문자 총 수를 계산하기 위해 aggregate, Sum을 이용하여 7일간 방문자 수를 더해서 계산.
        visit_records_total = VisitRecord.objects.filter(date__range=[seven_days_ago, today]).aggregate(total=Sum('count'))
        total_count = visit_records_total['total'] if visit_records_total['total'] is not None else 0

        # 각 방문 기록을 직렬화하여 JSON 형태로 변환.
        visit_records_data = [{'date': record.date.strftime('%Y-%m-%d'), 'count': record.count} for record in
                              visit_records]
        visit_records_json = json.dumps(visit_records_data)

        context = {
            'visit_records_json': visit_records_json,
            'today_records': today_records,
            'visit_records_total': total_count
        }

        return render(request, 'admin/main.html', context)

# 관리자 회원관리 페이지 View
class AdminMainUserView(View):
    def get(self, request):
        # 관리자 회원 관리 페이지로 이동
        return render(request, 'admin/main_user.html')


# 관리자 회원 관리 페이지, REST 방식을 이용한 ListAPI View
class AdminMainUserListAPI(APIView):
    def get(self, request, page):
        # 페이지에 표현할 행 개수 (5개)
        row_count = 5
        # 페이지 offset 설정
        offset = (page -1) * row_count
        # 페이지 limit 설정
        limit = page * row_count
        # 데이터베이스에서 가져올 column들을 지정
        columns = [
            'id',
            'member_email',
            'member_name',
            'member_phone',
            'created_date'
        ]
        # request에서 가져온 keyword(검색내용, default = '')
        keyword = request.GET.get('keyword', '')
        # 조건문 초기화
        condition = Q()
        # 검색 조건 설정 (회원 이름으로 검색하도록함)
        condition |= Q(member_name__icontains=keyword)

        # 검색 조건을 설정한 회원 목록을 가져옴.
        members = Member.objects.filter(condition).values(*columns)[offset:limit]
        # 총 회원 수를 설정
        total_count = Member.objects.count()
        # 대학생 회원의 목록(id)을 가져옴. flat=True 사용하여 단순한 값 목록을 가져온다.
        # (flat=True,는 QuerySet 값의 리스트를 반환할 때 사용되는 옵션)
        university_member_ids = list(University.objects.values_list('member', flat=True))
        # 학교 회원의 목록을 가져오되, 학교회원의 status또한 같이 가져온다.
        school_members = School.objects.values_list('member', 'school_member_status')

        for member in members:
            # 각 회원의 유형을 member-type의 이름으로 일반회원으로 지정해준다.
            member.setdefault('member-type', '일반회원')
            for school_member in school_members:
                # 만일 회원의 id값이 학교회원의 member와 같다면,
                if member['id'] == school_member[0]:
                    # 그 학교 회원 테이블에 있는 school_member_status값이 0이라면
                    if school_member[1] == 0:
                        # member-type은 학교 승인 대기중으로 지정
                        member['member-type'] = '학교 승인 대기중'
                    # 그 학교 회원 테이블에 있는 school_member_status 값이 1이라면,
                    elif school_member[1] == 1:
                        # member-type은 학교회원으로 지정
                        member['member-type'] = '학교회원'
                    # 학교회원임을 확인했기에 더이상 반복할 필요가 없어서 for 반복문 종료
                    break
                # 만일 회원이 대학생회원의 id 목록에 있다면
                elif member['id'] in university_member_ids:
                    # member-type은 대학생회원으로 지정한다.
                    member['member-type'] = '대학생회원'

        #  member_info에 나타낼 값들을 저장하고 전달.
        member_info = {
            'members' : members,
            'total_count' : total_count,

        }

        return Response(member_info)

# 학교 승인 대기중 -> 학교회원으로 status 전환
def translate(request):
    # POST method로 request를 받아온다면,
    if request.method == 'POST':
        # json 형태로 전달한 request의 body를 data에 저장.
        data = json.loads(request.body)
        # 전달된 data중, selected_items의 이름으로 전달된 datat를 selected_items로 저장.
        selected_items = data.get("selected_items")

        # selected_items는 id 값들을 받아오도록 설정했기에
        for item_id in selected_items:
            # selected_items중 item_id에 해당하는 member의 status를 True로 업데이트해준다.
            try:
                School.objects.filter(member=item_id).update(school_member_status=True)
            # 항목이 존재하지 않는 경우 무시
            except School.DoesNotExist:
                pass
        # 성공적으로 전환이 되었을경우 JsonResponse로 message를 전달
        return JsonResponse({'message': '선택된 항목이 성공적으로 전환되었습니다.'})
    # POST 방식으로 전달이 안되었을 경우 JsonResponse로 error message 전달.
    return JsonResponse({'error': 'POST 요청이 필요합니다.'}, status=400)

# 관리자 공지사항 View
class AdminMainNotificationView(View):
    def get(self, request):
        # 관리자 공지사항 페이지로 이동
        return render(request, 'admin/main_notification.html')

# 관리자 공지사항 관리 페이지, REST 방식을 이용한 ListAPI View
class AdminNotificationListAPI(APIView):
    def get(self, request, page):
        # 한 페이지에 표기할 행의 개수(5개)
        row_count = 5
        # 페이지 offset 설정
        offset = (page - 1) * row_count
        # 페이지 limit 설정
        limit = page * row_count
        # 데이터베이스에서 가져올 column 지정
        columns = [
            'id',
            'notification_title',
            'notification_status',
            'created_date',
            'notification_view_count'
        ]
        # 공지사항의 카테고리로 분류해서 표기위해 option값을 가져옴
        option = request.GET.get('option')
        # 만일 option값이 커뮤니티라면, filter로 커뮤니티에 해당되는 목록만 가져오고, 커뮤니티의 총 개수를 가져옴
        if option == '커뮤니티':
            notifications = Notification.enabled_objects.filter(notification_status=0).values(*columns)[offset:limit]
            total_count = Notification.enabled_objects.filter(notification_status=0).count()
        # option이 원랩 이라면, filter로 원랩에 해당되는 목록만 가져오고, 원랩의 총 개수를 가져옴
        elif option == '원랩':
            notifications = Notification.enabled_objects.filter(notification_status=1).values(*columns)[offset:limit]
            total_count = Notification.enabled_objects.filter(notification_status=1).count()
        # option이 장소공유 라면, filter로 장소공유에 해당되는 목록만 가져오고, 장소공유의 총 개수를 가져옴
        elif option == '장소공유':
            notifications = Notification.enabled_objects.filter(notification_status=2).values(*columns)[offset:limit]
            total_count = Notification.enabled_objects.filter(notification_status=2).count()
        # option이 공모전 이라면, filter로 공모전에 해당되는 목록만 가져오고, 공모전의 총 개수를 가져옴
        elif option == '공모전':
            notifications = Notification.enabled_objects.filter(notification_status=3).values(*columns)[offset:limit]
            total_count = Notification.enabled_objects.filter(notification_status=3).count()
        # 그 외의 option 이라면, 전체를 가져오도록 함.
        else:
            notifications = Notification.enabled_objects.values(*columns)[offset:limit]
            total_count = Notification.enabled_objects.count()


        # 화면으로 넘길 데이터를 notification_info에 저장.
        notification_info= {
            'notifications' : notifications,
            'total_count' : total_count
        }

        return Response(notification_info)

# 공지사항을 삭제하는 함수
def soft_delete(request):
    if request.method == 'POST':
        # JSON 형식으로 전달된 body의 데이터를 data에 저장.
        data = json.loads(request.body)
        # data중 selected_items의 이름의 데이터를 selected_items에 저장.
        selected_items = data.get("selected_items")

        # 선택된 항목들의 상태를 0으로 변경
        for item_id in selected_items:
            try:
                Notification.objects.filter(id=item_id).update(notification_post_status=False)
            # 항목이 존재하지 않는 경우 무시
            except Notification.DoesNotExist:
                pass
        # 성공적으로 삭제되었을때, message 반환
        return JsonResponse({'message': '선택된 항목이 성공적으로 삭제되었습니다.'})
    # POST방식으로 요청이 들어오지 않았을때 error 반환
    return JsonResponse({'error': 'POST 요청이 필요합니다.'}, status=400)


# 관리자 공모전 관리 페이지 View
class AdminMainExhibitionView(View):
    def get(self, request):
        # 관리자 공모전 관리 페이지로 이동
        return render(request, 'admin/main_exhibition.html')

# 관리자 공모전 관리 페에지, REST 방식을 이용한 ListAPI View
class AdminMainExhibitionListAPI(APIView):
    def get(self, request, page):
        # 한 페이지에서 표기할 행의 개수(5개)
        row_count = 5
        # 페이지 offset 설정
        offset = (page -1) * row_count
        # 페이지 limit 설정
        limit = page * row_count
        # 데이터베이스에서 가져올 column 지정
        columns = [
            'id',
            'exhibition_title',
            'exhibition_view_count',
            'school__member__member_name',
            'created_date'
        ]
        # annotate, F를 이용하여 school_member_name의 이름으로 school model에서 member model을 참조하여 그 이름을 가져옴.
        # enabled_objects 함수를 이용하여 status가 1인, 활성화된 값들만 가져오도록 함.
        exhibitions = Exhibition.enabled_objects\
                          .annotate(school_member_name=F('school__member__member_name')).values(*columns)[offset:limit]
        # 총 개수 count
        total_count = Exhibition.enabled_objects.count()
        # 페이지에 표기할 값들을 exhibition_info에 저장
        exhibition_info = {
            'exhibitions' : exhibitions,
            'total_count' : total_count
        }

        return Response(exhibition_info)

# exhibition을 soft_delete하기위해 만든 함수
def soft_delete_exhibition(request):
    if request.method == 'POST':
        # JSON 형식으로 전달된 body의 데이터를 data에 저장
        data = json.loads(request.body)
        # data중 selected_items 이름의 데이터를 selected_items에 저장
        selected_items = data.get("selected_items")

        # 선택된 항목들의 상태를 0으로 변경
        for item_id in selected_items:
            try:
                Exhibition.objects.filter(id=item_id).update(exhibition_post_status=False)
            # 항목이 존재하지 않는 경우 무시
            except Exhibition.DoesNotExist:
                pass
        # 성공적으로 status가 전환되었을 때, JsonResponse로 반환할 message
        return JsonResponse({'message': '선택된 항목이 성공적으로 삭제되었습니다.'})
    # POST 방식으로 요청이 들어오지 않을때 반환할 error message
    return JsonResponse({'error': 'POST 요청이 필요합니다.'}, status=400)

# 관리자 로그아웃 View
class AdminMainLogoutView(View):
    def get(self, request):
        request.session.clear()
        return redirect('/')
