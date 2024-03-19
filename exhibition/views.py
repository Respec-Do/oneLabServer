import mimetypes
from urllib.parse import quote
from django.utils.encoding import iri_to_uri

from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.views import View

from exhibition.models import Exhibition, ExhibitionFile
from exhibitionMember.models import ExhibitionMember
from file.models import File
from member.models import Member
from school.models import School
from university.models import University

# 공모전 작성 View
class ExhibitionWriteView(View):
    # 공모전 작성페이지로 render 방식으로 전달
    def get(self, request):
        return render(request, 'exhibition/write.html')

    # 작성할 때, 오류가 발생할 경우 롤백하기 위해 transaction.atomic 사용
    @transaction.atomic
    def post(self, request):
        # data에 POST방식으로 담은 데이터를 전달
        data = request.POST
        # 로그인한 회원의 정보를 받아옴.
        member = Member(**request.session['member'])
        school = School.objects.get(member=member)

        # data라는 이름으로 request를 통해 입력한 값을 저장.
        data = {
            'exhibition_title': data['exhibition-title'],
            'exhibition_content': data['exhibition-content'],
            'school': school,
            'exhibition_url': data['exhibition-url']
        }
        # exhibition 데이터 생성
        exhibition = Exhibition.objects.create(**data)
        # 공모전 사이트를 통해 이미지파일을 담아오기 위해 key와 file로 구분
        for key, file in request.FILES.items():
            # exhibition_file은 File을 foreignkey로 받아옴.
            file_instance = File.objects.create(file_size=file.size)
            # 다운로드할 파일과 이미지 저장을 구분하기 위해, key==upload4로 저장된 파일은 다운로드파일로 따로 저장
            if key == 'upload4':  # upload4 파일이면 download_path 필드에 저장
                ExhibitionFile.objects.create(file=file_instance, path=None, download_path=file, preview=False,
                                              exhibition=exhibition)
            # 다운로드할 파일이 아닌 이미지 업로드용 파일 중, 미리보기 및 대표 이미지로 지정할 이미지는 key값이 upload1로 preview로 지정
            else:
                ExhibitionFile.objects.create(file=file_instance, path=file, download_path=None, preview=key=='upload1',
                                              exhibition=exhibition)
        # 저장이 되었기에, 상세보기 페이지로 이동.
        return redirect(exhibition.get_absolute_url())

# 공모전 상세보기 View
class ExhibitionDetailView(View):
    def get(self, request):
        # get으로 request로 전달한 id 값의 Exhibition을 읽어온다.
        exhibition = Exhibition.objects.get(id=request.GET['id'])
        school = exhibition.school
        # 작성자의 이름을 확인하기 위해, exhibition은 school을 school은 member를 참조한다.
        member = school.member
        # 페이지의 조회수, 상세보기페이지로 들어올 때마다 조회수가 1씩 증가
        exhibition.exhibition_view_count += 1
        # 증가한 조회수를 저장함.
        exhibition.save(update_fields=['exhibition_view_count'])
        # 위에서 찾아온 값들을 화면에 뿌리기 위해, context에 저장.
        context = {
            'exhibition' : exhibition,
            'exhibition_files' : list(exhibition.exhibitionfile_set.all()),
            'member_name' : member.member_name
        }

        return render(request, 'exhibition/detail.html', context)
    def post(self, request):
        data = request.POST
        member_id = request.session['member']['id']
        university = University.objects.get(member_id=member_id)

        if university is None:
            return render(request, 'exhibition/detail.html', {'error': '대학생만 참여 가능합니다.'})

        exhibition_id = data.get('id')

        # 이미 참여한 공모전인지 확인
        existing_member = ExhibitionMember.objects.filter(university_id=university.member_id,
                                                          exhibition_id=exhibition_id).first()
        if existing_member:
            # 이미 참여한 경우에는 업데이트 시간만 변경

            from django.utils import timezone
            existing_member.updated_at = timezone.now()
            existing_member.save()
        else:
            # 참여한 공모전이 없는 경우에만 새로운 데이터 생성
            datas = {
                'university_id': university.member_id,
                'exhibition_id': exhibition_id,
                'exhibition_member_status': 0
            }
            ExhibitionMember.objects.create(**datas)

        return redirect('myPage:main')

# 공모전 양식 파일 다운로드 View
class ExhibitionFileDownloadView(View):
    def get(self, request, file_path, *args, **kwargs):
        # file_path: 파일이 있는 경로 설정, 파일이름은 경로에 포함
        file_path = file_path
        # 파일 경로에서 파일 이름을 추출
        file_name = file_path.split('/')[-1]
        # FileSystemStorage라는 클래스를 불러옴.
        fs = FileSystemStorage()
        # 파일 이름을 기반으로 파일의 MIME 타입을 추측
        content_type, _ = mimetypes.guess_type(file_name)
        # FileSystemStorage를 사용하여 파일을 열고 FileResponse를 준비
        # 'rb'는 파일을 이진(binary)로 읽기위한 옵션
        # content_type은 HTTP응답에 포함될 파일의 MIME 타입을 지정.
        response = FileResponse(fs.open(file_path, 'rb'),
                                content_type=content_type)
        # 파일 이름을 인코딩해서 HTTP 헤더에서 특수 문자 처리
        encoded_file_name = quote(file_name)
        # Content-Disposition 헤더를 설정해서 다운로드를 위해 원래 파일 이름으로 표시
        response['Content-Disposition'] = f'attachment; filename="{encoded_file_name}"; filename*=UTF-8\'\'{encoded_file_name}'
        return response

# 공모전 목록 View
class ExhibitionListView(View):
    def get(self, request):
        # 로그인한 회원의 정보를 가져옴
        member = Member(**request.session['member'])
        # 활성화된 공모전의 목록을 enabled_objects manager를 통해 status가 1인 공모전만 가져옴.
        context = {
            'exhibitions' : list(Exhibition.enabled_objects.all()),
            'member' : member
        }
        # 목록페이지로 context 담아서 이동
        return render(request, 'exhibition/list.html', context)

# 공모전 수정페이지 View
class ExhibitionUpdateView(View):
    # html 페이지에서 수정할 페이지의 id를 전달
    def get(self, request, id):
        # get id 를 통해 수정할 공모전을 가져옴
        exhibition = Exhibition.objects.get(id=id)
        # 수정할 공모전의 파일도 같이 가져옴
        exhibitionfiles = ExhibitionFile.objects.filter(exhibition=exhibition)

        context = {
            'exhibition' : exhibition,
            'exhibition_files' : exhibitionfiles,

        }
        # 수정할 내용을 표기하기 위해 context에 담아서 전달
        return render(request, 'exhibition/update.html', context)

    # 수정할 때, 오류가 날 경우 롤백을 위해 transaction.atomic을 사용
    @transaction.atomic
    def post(self, request, id):
        # POST방식으로 data를 받아옴.
        data = request.POST
        # 수정할 공모전을 id를 통해 가져온다.
        exhibition = Exhibition.objects.get(id=id)
        # 수정할 내용을 저장해준다.
        exhibition.exhibition_title = data['exhibition-title']
        exhibition.exhibition_content = data['exhibition-content']
        exhibition.exhibition_url = data['exhibition-url']
        # save, update_fields를 통해 수정한 내용을 업데이트 해준다.
        exhibition.save(update_fields=['exhibition_title', 'exhibition_content', 'exhibition_url'])
        # 기존에 남아있던 해당 공모전의 파일들은 다 제거해준다.
        exhibition.exhibitionfile_set.all().delete()
        # 요청을 통해 전달된 파일들을 key와 file로 구분
        for key, file in request.FILES.items():
            file_instance = File.objects.create(file_size=file.size)
            # upload4 파일이면 download_path 필드에 저장
            if key == 'upload4':
                ExhibitionFile.objects.create(file=file_instance, path=None, download_path=file, preview=False,
                                              exhibition=exhibition)
            # 나머지 파일들을 저장할 떄, 대표이미지및 미리보기로 표기할 이미지 파일은 preview값을 1로 지정.
            else:
                ExhibitionFile.objects.create(file=file_instance, path=file, download_path=None, preview=key=='upload1',
                                              exhibition=exhibition)
        # 수정이 완료된 페이지는 다시 get_absolute_url 를 통해 상세보기 페이지로 이동.
        return redirect(exhibition.get_absolute_url())