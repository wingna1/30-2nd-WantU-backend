# 원티드 Project

![image](https://user-images.githubusercontent.com/60123530/160071116-4ae9642a-edf8-4fc5-be4c-6eec0620a02e.png)

## 프로젝트 소개

- WantU는 리크루팅 서비스를 제공하는 원티드를 모티브로 구현한 웹 사이트 서비스입니다.
- 짧은 프로젝트 기간동안 개발에 집중하기 위해 기획 및 기능의 일정 부분을 비슷하게 구현했습니다.

### 프로젝트 인원

- **프론트엔드: 박별, 전슬기**  
- **백엔드: 박영서, 이예솔**

### 프로젝트 작업기간

2022.03.14 ~ 2022.03.25

### 시연 영상



### DB modeling

![image](https://user-images.githubusercontent.com/60123530/160071035-f963edc5-1b8b-4d64-bc86-b2cf387e5d8a.png)

## 적용 기술 및 구현 기능

### 적용 기술

> - Front-End: React.js, sass, HTML
> - Back-End: Python, Django web fremework, AWS, Kakao API, Docker, MySQL

### 구현 기능

#### 회원가입, 로그인 

- 회원가입, 로그인: 카카오에서 인가 코드 및 액세스 토큰을 발급받아 서버에 기등록된 회원인지를 확인한 후 등록되지 않았을 경우 새로 가입하고 등록된 회원일 경우 id 외에 이메일이나 프로필 이미지 url같은 다른 정보를 업데이트한 후 서버 토큰을 발급해 유저 정보와 함께 제공

#### 상품 리스트

- Q객체를 사용해 카테고리별, 태그별, 회사 위치별 필터링
- 공고 제목순, 등록일순, 마감일순 정렬
- 페이지네이션 : offset과 limit를 받아 해당되는 데이터를 제공

#### 상품 상세 페이지

- 공고에 대한 상세 정보와 공고를 등록한 회사에 대한 정보를 제공
- 로그인한 유저의 경우 해당 공고에 지원했는지에 대한 여부와 이력서 작성에 필요한 이름, 이메일 등 데이터 제공
- 지원하기 기능을 통하여 본인의 이력서 중 원하는 이력서를 선택하여 해당 직무에 지원 가능 

#### 마이 페이지
- 유저의 지원 정보를 지원 상태(지원 완료, 서류 합격, 불합격, 최종합격) 에 따라 분리하여 각 횟수를 보여줌
- 각 지원 상태를 클릭할 시 구체적인 지원 정보가 나옴(회사명, 지원 일자, 직군, 지원 상태)
- S3 버킷을 이용하여 본인의 이력서를 등록, 이름 변경, 삭제 
- 등록된 이력서 리스트를 보여줌 

## Reference
- 이 프로젝트는 원티드 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
