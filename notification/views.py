from django.db import transaction
from django.db.models import Q, Subquery, OuterRef
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from file.models import File
from notification.models import Notification, NotificationFile

# 공지사항 작성 View
class NotificationWriteView(View):
    def get(self, request):
        # render로 공지사항 작성하는 페이지로 이동
        return render(request, 'notification/write.html')

    # 공지사항 작성시, 에러발생할 경우 롤백을 위해 transaction.atomic 사용.
    @transaction.atomic
    def post(self, request):
        # POST 메소드로 데이터를 받아온다.
        data = request.POST
        file = request.FILES
        # 공지사항의 제목, 내용, 공지사항의 유형(status)을 data에 담는다.
        data = {
            'notification_title': data['notification-title'],
            'notification_content': data['notification-content'],
            'notification_status': data['notification-status']
        }
        # 받아온 데이터를 create로 만들어준다.
        notification = Notification.objects.create(**data)

        # 요청으로 받아온 이미지파일
        for key, file in request.FILES.items():
            # File을 FK로 받고있기에 파일크기를 나타내는 file_instance를 먼저 생성
            file_instance = File.objects.create(file_size=file.size)
            # 업로드한 이미지파일 NotificationFile 에 생성
            NotificationFile.objects.create(file=file_instance, path=file, notification=notification)
        # 작성 완료후 get_absolute_url을 통해 상세보기로 이동.
        return redirect(notification.get_absolute_url())


# 공지사항 상세보기 View
class NotificationDetailView(View):
    def get(self, request):
        # request.GET 메소드로 받아온 id 값으로 해당되는 공지사항을 찾아온다.
        notification = Notification.objects.get(id=request.GET['id'])
        # 공지사항 상세보기페이지 들어갈때마다 조회수 증가
        notification.notification_view_count += 1
        # 증가된 조회수를 update함.
        notification.save(update_fields=['notification_view_count'])
        # 해당되는 공지사항과 그 공지사항의 파일들을 context에 담는다.
        context = {
            'notification' : notification,
            'notification_file' : list(notification.notificationfile_set.all())
        }
        # render방식으로 상세보기 페이지로 이동.
        return render(request, 'notification/detail.html', context)

# 공지사항 목록 보기 View
class NotificationListView(View):
    def get(self, request):
        # 공지사항 목록 보기페이지로 이동
        return render(request, 'notification/list.html')

# 공지사항 목록의 ListAPI View
class NotificationListAPI(APIView):
    def get(self, request, page):
        # 표기할 행의 개수 (5개)
        row_count=5
        # 페이지 오프셋 설정
        offset = (page -1) *  row_count
        # 페이지 제한을 설정
        limit = page * row_count

        # 데이터베이스에서 가져올 열 지정
        columns = [
            'id',
            'notification_title',
            'notification_content',
            'notification_view_count',
            'notification_status',
            'created_date',
            'notification_file'
        ]
        # request에서 받아온 category값 default=0
        category = request.GET.get('category', 0)
        # request에서 받아온 type (검색 타입에 해당한다)
        type = request.GET.get('type', '')
        # request에서 받아온 keyword(검색 내용에 해당한다)
        keyword = request.GET.get('keyword', '')

        # 조건문 초기화
        condition = Q()
        # type에 따라 검색 조건을 설정
        if type:
            for t in list(type):
                # 검색 조건이 제목일 경우
                if t == 't':
                    condition |= Q(notification_title__icontains=keyword)
                # 검색 조건이 내용일 경우
                elif t == 'c':
                    condition |= Q(notification_content__icontains=keyword)
                # 검색 조건이 제목+내용일 경우
                elif t =='tc':
                    condition |= Q(notification_title__icontains=keyword) & Q(notification_content__icontains=keyword)

        # 필터링된 공지사항을 가져온다. annotate를 이용하여 notification_file의 경로를 지정하여 이미지파일도 가져온다.
        notifications = Notification.enabled_objects.filter(notification_status=category).filter(condition).annotate(
            notification_file=Subquery(NotificationFile.objects.filter(notification=OuterRef('pk')).values('path')[:1])
        ).values(*columns)[offset:limit]
        # 다음 페이지 존재 여부를 확인한다.
        has_next = Notification.enabled_objects.filter().filter(condition)[limit:limit + 1].exists()
        # notification_info에 저장하여 반환.
        notification_info = {
            'notifications' : notifications,
            'hasNext' : has_next
        }

        return Response(notification_info)

# 공지사항 수정 View
class NotificationUpdateView(View):
    def get(self, request, id):
        # get으로 id값을 전달받고 그 값으로 수정할 공지사항을 찾는다.
        notification = Notification.objects.get(id=id)
        # context에 id를 통해 찾은 공지사항과, 그 파일들을 담아준다.
        context = {
            'notification' : notification,
            'notification_file' : notification.notificationfile_set.all()
        }
        # render방식으로 수정할 페이지로 context와 함께 이동.
        return render(request, 'notification/update.html', context)

    # 수정할때 오류가 났을 경우 롤백하기 위해 transaction.atomic을 사용
    @transaction.atomic
    def post(self, request, id):
        data = request.POST
        file = request.FILES
        # id값을 통해 수정할 공지사항을 찾는다.
        notification = Notification.objects.get(id=id)
        # 수정한 제목, 수정한 내용, 수정한 공지사항의 종류를 지정해준다.
        notification.notification_title = data['notification-title']
        notification.notification_content = data['notification-content']
        notification.notification_status = data['notification-status']
        # save, update_fields를 통해 수정한 내용을 저장.
        notification.save(update_fields=['notification_title', 'notification_content', 'notification_status'])
        # 수정한 공지사항의 기존 파일들은 제거
        notification.notificationfile_set.all().delete()
        # 요청으로 받아온 파일을 저장
        for key, file in request.FILES.items():
            file_instance = File.objects.create(file_size=file.size)
            NotificationFile.objects.create(file=file_instance, path=file, notification=notification)
        # 수정작업이 완료된 이후 redirect로 수정된 공지사항의 상세보기로 이동.
        return redirect(notification.get_absolute_url())