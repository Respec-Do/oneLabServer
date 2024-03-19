from django.db import models

from exhibition.managers import ExhibitionManager
from file.models import File
from like.models import Like
from oneLabProject.models import Period
from school.models import School


class Exhibition(Period):
    # 공모전 제목
    exhibition_title = models.CharField(null=False, max_length=40)
    # 공모전 내용
    exhibition_content = models.CharField(null=False, max_length=2000)
    # False=관리자, True=school
    exhibition_status = models.BooleanField(null=False, blank=False, default=True)
    # 학교회원
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    # True=게시 중, False=게시 종료
    exhibition_post_status = models.BooleanField(null=False, default=True)
    # 공모전 url
    exhibition_url = models.TextField(null=False, blank=False)
    # 공모전 페이지의 조회수
    exhibition_view_count = models.IntegerField(null=False, blank=False, default=0)

    objects = models.Manager()
    # enabled_objects를 통해 exhibition_post_status가 1인, 즉 활성화된 공모전만 가져오도록 하기위한 함수.
    enabled_objects = ExhibitionManager()


    class Meta:
        db_table = 'tbl_exhibition'
        ordering = ['-id']

    # get_absolute_url을 통해 상세보기로 바로 이동할 수 있도록 일괄화처리.
    def get_absolute_url(self):
        return f'/exhibition/detail/?id={self.id}'

class ExhibitionFile(Period):
    # File 을 슈퍼키로 지정해서 FK로 받아온다.
    file = models.ForeignKey(File, primary_key=True, on_delete=models.PROTECT, null=False)
    # 파일이 저장될 경로
    path = models.ImageField(null=False, blank=False, upload_to='exhibition/%Y/%m/%d')
    # 공모전을 FK로 받아와서 해당 공모전의 파일만 가져오도록 한다.
    exhibition = models.ForeignKey(Exhibition, on_delete=models.PROTECT, null=False)
    # 공모전 양식 파일을 담을 경로
    download_path = models.ImageField(null=False, blank=False, upload_to='exhibition_down/%Y/%m/%d')
    # 대표 이미지, 및 미리보기. preview=key=='' 식으로 지정
    preview = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_exhibition_file'

class ExhibitionLike(Period):
    like = models.ForeignKey(Like, primary_key=True, on_delete=models.PROTECT, null=False)
    class Meta:
        db_table = 'tbl_exhibition_like'