# like_lion_first_project_twitter
## 🌐 배포 웹사이트 : <br>https://likelionfirstprojecttwitter-main-ken.streamlit.app/  


# 다운로드 
```
git clone https://github.com/ken-do-it/like_lion_first_project_twitter

```
# 설치 환경
```
 git install requirement.txt
 
(streamlit==1.48.0,  pandas==2.3.1)
```
# 실행 명령어
``` 
streamlit run app.py 
```

# 디렉터리 구조
```
project/
├─ app.py                  # 메인 Streamlit 앱
├─ auth.py                 # 로그인/회원가입 UI
├─ user_manager.py         # 사용자 관리(CSV)
├─ post_manager.py         # 포스트/좋아요/리트윗 관리
├─ skills_manager.py       # 스킬(기술 스택) 관리
├─ setup_data.py           # data 폴더와 초기 CSV 생성 스크립트
└─ data/                   # CSV 저장 폴더(자동 생성)
```

# 데이터 
## users.csv
| 컬럼명            | 설명                   | 예시 값                             |
| -------------- | -------------------- | -------------------------------- |
| user\_id       | 내부 식별자 (user\_001 …) | user\_001                        |
| user\_name     | 사용자명 (로그인 ID)        | alice                            |
| password       | 비밀번호 (📌 현재는 평문)     | 1234                             |
| created\_at    | 가입일 (YYYY-MM-DD)     | 2025-08-18                       |
| profile\_image | 프로필 이미지 URL          | [https://...jpg](https://...jpg) |
---
<br>
<br>

## posts.csv
| 컬럼명                | 설명                               | 예시 값                |
| ------------------ | -------------------------------- | ------------------- |
| post\_id           | 게시글 ID (8자리 uuid)                | ab12cd34            |
| user\_id           | 작성자 user\_id                     | user\_001           |
| content            | 게시글 내용                           | "안녕하세요"             |
| time\_stamp        | 작성/수정 시각 (YYYY-MM-DD HH\:MM\:SS) | 2025-08-18 14:22:00 |
| is\_retweet        | 리트윗 여부 (True/False)              | False               |
| original\_post\_id | 원글 post\_id (리트윗일 때만)            | ab12cd34            |

---
<br>
<br>

## likes.csv
| 컬럼명         | 설명                | 예시 값                |
| ----------- | ----------------- | ------------------- |
| like\_id    | 좋아요 ID (8자리 uuid) | lk12ab34            |
| user\_id    | 좋아요 누른 사용자 ID     | user\_002           |
| post\_id    | 좋아요 대상 게시글 ID     | ab12cd34            |
| time\_stamp | 좋아요 누른 시각         | 2025-08-18 15:10:00 |


<br>
<br>

## skills.csv 

| 컬럼명         | 설명               | 예시 값                |
| ----------- | ---------------- | ------------------- |
| skill\_id   | 스킬 ID (8자리 uuid) | sk12ab34            |
| user\_id    | 소유자 user\_id     | user\_001           |
| user\_name  | 사용자명             | alice               |
| skill\_name | 스킬명              | Python              |
| level       | 숙련도 (0\~100 정수)  | 80                  |
| created\_at | 스킬 추가 시각         | 2025-08-18 13:00:00 |
| updated\_at | 스킬 마지막 수정 시각     | 2025-08-18 13:30:00 |

<br>
<br>
<br>
<br>



# 로그인, 회원가입 페이지
다른 조건은 없고 계정이 없으면 회원가입을 먼저 해야한다 
![alt text](/image_all/image-firstpage.png)

- 처음 들어오면 로그인 페이지 접속 
- 아이디 유무에 따라 회원가입 필요 
<br>
<br>
<br>
<br>


# 홈 페이지
![alt text](/image_all/image-homepage.png)
### tab을 활용해서 내가 쓴글, 리트윗한 글, 내가 좋아요한 글 을 따로 모아서 볼 수 있다   

# 프로필 
![alt text](/image_all/image-profile.png)

### 내 기술을 등록 및 수정이 가능하다 
### 프로필 사진을 URL 주소로 변경이 가능하고 제시된 사진을 선택가능




