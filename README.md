<h1>ONELAB</h1> 

- 전국 대학 통합을 통한 교육수준 상향 평준화를 위한 플랫폼

<h2>✔️프로젝트 소개</h2>
<img width="960" alt="슬라이드0001" src="https://github.com/Respec-Do/study_python/assets/105579519/b83b8443-3f3c-4082-a399-a6a3748bfa1d">

- 'ONELAB'은 국내 대학 통합을 통해 교육 수준 상향 평준화를 지향하는 웹 플랫폼입니다.
- 모든 대학생들이 자유로이 사용할 수 있는 웹 플랫폼을 구현해보았습니다.

<h2>✔️기획 배경</h2>

<h3>벛꽃이 피는 순서대로 대학이 사라진다</h3>

- 이 말은 한국의 수도권에 위치한 대학들은 높은 교육 품질과 인프라가 구축되어 있어 학생들의 선호도가 매우 높지만, 지방 대학들은 교수진 부족 및 연구 인프라의 부족, 지역사회와의 유기적인 연계 부재 등으로 선호도가 낮아, 사라질 위기에 놓여 있다는 의미를 내포하고 있습니다.
<img width="960" alt="슬라이드0004" src="https://github.com/Respec-Do/study_python/assets/105579519/8ce17ce8-8f32-4ca9-a4fc-32eb0c329443">

<h3>지방대학의 60%가 사라진다.</h3>

- 교육부의 발표에 따르면 대학의 생존율이 낮아지고 있으며, 지방 대학의 경우 60%가 사라질 것으로 예측되고 있습니다. 이와 비교해서, 학령인구 감소에도 불구하고 상위권 대학 경쟁률은 상승하고 있다는 것을 볼 수 있습니다.
<img width="960" alt="슬라이드0005" src="https://github.com/Respec-Do/study_python/assets/105579519/81345db1-0b8a-41e3-98b4-a5d69bb341b9">

<h3>실제 다른 대학의 플랫폼에 참여하고 싶어하는 대학생들</h3>

- 실제 웹 상에서도 많은 대학생들이 다른 대학교의 플랫폼에 참여하고 싶어하는 모습을 확인할 수 있었습니다.
<img width="960" alt="슬라이드0006" src="https://github.com/Respec-Do/study_python/assets/105579519/f710f703-55a5-4d95-9b53-db4045d136bc">

- 이와 같은 이유들로 대학 통합을 통한 교육 수준 상향 평준화 플랫폼을 기획하게 되었습니다.

<h2>✔️기대 효과</h2>

<img width="960" alt="슬라이드0007" src="https://github.com/Respec-Do/study_python/assets/105579519/b8d7597c-c12f-4c95-8d99-5df5d102210c">

- 여러 대학생들의 자료, 대학교의 공간, 정보 등을 공유함으로써 교육의 품질을 향상시킬 수 있습니다.
- 이를 통해 교육 수준을 높이고, 교육의 품질을 균일하게 유지하며, 교육의 상향 평준화를 이룰 수 있습니다.
- 모두에게 교육의 기회를 공평하게 제공할 수 있습니다.


<h2>✔️개발 기간</h2>

- 퍼블리싱 : 2024.02.01 ~ 2024.02.16
- 프로젝트 기획
- ERD 제작
- 업무 분담
- 서버 작업 : 2024.02.29 ~ 2024.03.17
- 프로젝트 발표 : 2024.03.18

<h2>✔️팀 구성원 소개 및 역할</h2>

<div align='center'>

||박유진|문우람|이기영|도강현|임소영|조성현|
|:-----:|:-----:|:-----:|:------:|:------:|:------:|:------:|
|역할|팀장|부팀장|서버관리|팀원|팀원|팀원|
|Front|메인페이지<br>로그인<br>회원가입|학교<br>공모전<br>장소공유<br>결제하기|계정찾기<br>비밀번호 재설정<br>회사소개|마이페이지<br>결제확인|원랩<br>자료요청<br>커뮤니티|공지사항<br>관리자페이지|
|Back||로그인<br>회원가입<br>계정찾기<br>메인페이지|원랩<br>커뮤니티<br>서버 관리|공모전<br>관리자<br>공지사항|학교<br>장소공유<br>자료공유|마이페이지<br>결제|
  
</div>

<h4>✔️Front-End</h4>

<img width="960" alt="슬라이드0003" src="https://github.com/Respec-Do/django-server/assets/105579519/4d28c965-6ec8-4359-924d-3b6ba90dbd3a">

<h4>✔️Back-End</h4>

<img width="960" alt="슬라이드0003" src="https://github.com/Respec-Do/django-server/assets/105579519/25515065-6e84-4769-b100-86fa590190c1">

<h2>✔️퍼블리싱 작업</h2>

- 마이페이지
- 포인트 확인

### ✔️퍼블리싱 진행률

<img width="960" alt="front 진행도" src="https://github.com/Respec-Do/django-server/assets/105579519/90e4771f-8931-4913-8ac4-e481474cd921">

## ✔️마이페이지/포인트 확인

### ✔️마이페이지

- 마이페이지, 모달창 및 탭별 목록 보기 구현

#### ✔️View

<details>
<summary>마이페이지</summary>
<div markdown="1">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/dfb6eed6-61a9-403a-8b0c-1114fde8faca "/>

</div>
</details>

<details>
<summary>프로필변경 모달</summary>
<div markdown="2">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/6706583d-aa28-4341-b360-c2819d2ffcde" />
</div>
</details>

<details>
<summary>이메일 인증 모달</summary>
<div markdown="3">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/3a2987ed-982d-4367-9632-1dfd8f60641e" />
</div>
</details>
<details>
<summary>원랩 -> 랩장</summary>
<div markdown="4">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/ad6e5aea-62ba-4702-b61b-32ddfc4746ae" />
</div>
</details>

<details>
<summary>원랩 -> 랩장 -> 관리하기</summary>
<div markdown="5">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/e2873874-52fb-4918-aabf-fd1136c2170c" />
</div>
</details>

<details>
<summary>원랩 -> 랩원</summary>
<div markdown="6">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/489daffa-f8f3-431e-bae9-524c651cad0b" />
</div>
</details>

<details>
<summary>자료 공유</summary>
<div markdown="7">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/aa5e7cf4-0bbf-42e0-aef4-ff7dda490dc5" />
</div>
</details>

<details>
<summary>장소 공유</summary>
<div markdown="8">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/b8aae60c-dda4-4df6-a4f9-d8f5e5239f6c" />
</div>
</details>

<details>
<summary>공모전/대회</summary>
<div markdown="9">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/c03d630b-8ca6-4a9a-8ad4-7eb997389671" />
</div>
</details>

<details>
<summary>커뮤니티</summary>
<div markdown="10">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/31ce96d6-dbff-4621-a90c-2ec8327065e9" />
</div>
</details>

### ✔️포인트 확인

- 포인트 결제, 적립, 사용 내역

#### ✔️View

<details>
<summary>포인트 충전</summary>
<div markdown="11">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/91a54151-2fd2-4878-abcd-bc21ed94a670"/>

</div>
</details>

<details>
<summary>포인트 적립</summary>
<div markdown="12">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/53d9aabb-8e5f-4ddf-9b16-2d27210fdbb8"/>

</div>
</details>
<details>
<summary>포인트 사용</summary>
<div markdown="13">

<img src="https://github.com/Respec-Do/django-server/assets/105579519/0b6b4ceb-c29d-436d-b1cf-350bfa7d37ea"/>

</div>
</details>


<h2>프로젝트에서 느낀 점</h2>

<h3>어려웠던 부분</h3>

<h3>문제를 해결했던 부분</h3>














