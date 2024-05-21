import os
import csv
import django
from django.utils import timezone

# Django 프로젝트 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oneLabProject.settings")
django.setup()

from onelab.models import OneLab
from university.models import University
from community.models import Community

# 기본값 설정

# CSV 파일 읽기 및 데이터 삽입
with open('data.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        community = Community(
            community_title=row[0],  # 'onelab_main_title'는 첫 번째 열에 위치한다고 가정
            community_content=row[1],  # 'onelab_content'는 두 번째 열에 위치한다고 가정
            status=False,
            post_status=row[3],  # 'onelab_detail_content'는 세 번째 열에 위치한다고 가정
            member_id=2

        )
        community.save()
        print(f"Inserted: {community.community_title}")








