import streamlit as st
import pandas as pd
from auth import show_auth_page, logout_user
from user_manager import UserManager
from post_manager import PostManager

st.markdown(
    """
    <style>
    /* st.button의 래퍼 div 자체를 인라인으로 만들어 옆으로 붙게 하기 */
    div.stButton {
        display: inline-block;   /* 핵심! */
        margin-right: 6px;       /* 버튼 사이 간격 */
        margin-bottom: 0;        /* 아래 여백 제거해 세로로 안 밀리게 */
    }
    /* 버튼 자체 크기만 살짝 줄이기(선택) */
    div.stButton > button {
        padding: 0.35rem 0.55rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.set_page_config(
    page_title="개발 유니콘다",
    page_icon="🦄",
    layout='wide',
    initial_sidebar_state="auto",  # 'auto' | 'expanded' | 'collapsed'
    menu_items={                  # 우상단 메뉴 커스터마이즈
        "Get Help": "https://likelionfirstprojecttwitter-main.streamlit.app/",
        "Report a bug": "mailto:you@example.com",
        "About": "파이썬 트위터 프로젝트 - 간단한 SNS 데모"
    }
)

def show_home_page(current_user, post_mgr, user_mgr):
    """홈 화면 - 실제 게시글 목록"""
    # 안전장치: 매개변수 확인
    if current_user is None or 'user_id' not in current_user:
        st.error("사용자 정보가 올바르지 않습니다.")
        return
    
    if post_mgr is None:
        st.error("포스트 매니저가 초기화되지 않았습니다.")
        return
    
    if user_mgr is None:
        st.error("사용자 매니저가 초기화되지 않았습니다.")
        return
    
    st.header("📝 최근 프롬프트")

    # 게시글 불러오기
    posts_with_likes = post_mgr.get_posts_with_likes()

    if len(posts_with_likes) == 0:
        st.info("📝 아직 작성된 프롬프트가 없습니다. 첫 번째 프롬프트를 작성해보세요!")
        if st.button("✍️ 글쓰기로 이동"):
            st.session_state.menu = "✍️ 글쓰기"
            st.rerun()
        return
    

    # 사용자 이름 가져오기 위해 users와 조인
    users_df = user_mgr.load_users()
    posts_display = posts_with_likes.merge(
        users_df[['user_id', 'user_name']],
        on='user_id',
        how='left'
    )



        # 게시글 하나씩 표시
    for idx, post in posts_display.iterrows():
        with st.container():
            # 프로필 이미지와 정보
            col1, col2 = st.columns([1, 11])

            with col1:
                st.image("https://images.unsplash.com/photo-1743449661678-c22cd73b338a?w=500&auto=format&fit=crop&q=60", width=50)

            with col2:
                # 사용자 이름 + 시간
                time_stamp = post['time_stamp']
                if pd.isna(time_stamp):
                    time_str = "시간 정보 없음"
                else:
                    try:
                        time_str = str(time_stamp).split(' ')[1][:5]  # HH:MM
                    except (AttributeError, IndexError):
                        time_str = "시간 오류"
                st.markdown(f"**{post['user_name']}** • {time_str}")

                # 게시글 내용 (수정 모드 / 일반 모드)
                if st.session_state.get('editing_post') == post['post_id']:
                    with st.form(f"edit_form_{post['post_id']}", clear_on_submit=False):
                        edited_content = st.text_area(
                            "내용 수정",
                            value=str(post['content']) if pd.notna(post['content']) else "",
                            height=100,
                            key=f"edit_content_{post['post_id']}"
                        )
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 저장"):
                                if edited_content and edited_content.strip():
                                    if post_mgr.update_post(post['post_id'], current_user['user_id'], edited_content.strip()):
                                        st.success("수정되었습니다!")
                                        st.session_state.editing_post = None
                                        st.rerun()
                                else:
                                    st.error("내용을 입력해주세요!")
                        with col_cancel:
                            if st.form_submit_button("❌ 취소"):
                                st.session_state.editing_post = None
                                st.rerun()
                else:
                    if post.get('is_retweet', False):
                        st.markdown(f"🔁 **리트윗:** {post['content']}")
                    else:
                        st.markdown(post['content'])

                # -------------------
                # 액션바 (좋아요 | 수정 | 삭제 | 리트윗)
                # -------------------
                is_liked = post_mgr.is_liked_by_user(current_user['user_id'], post['post_id'])
                like_emoji = "❤️" if is_liked else "🤍"
                like_count = int(post['like_count'])

                # 버튼을 가로로 나란히 배치 + 약간의 간격
                btn_cols = st.columns(4, gap="small")

                with btn_cols[0]:
                    if st.button(f"{like_emoji} {like_count}", key=f"like_{post['post_id']}"):
                        liked = post_mgr.toggle_like(current_user['user_id'], post['post_id'])
                        st.success("좋아요!") if liked else st.info("좋아요 취소")
                        st.rerun()

                with btn_cols[1]:
                    if post['user_id'] == current_user['user_id']:
                        if st.button("✏️", key=f"edit_{post['post_id']}", help="수정"):
                            st.session_state.editing_post = post['post_id']
                            st.rerun()

                with btn_cols[2]:
                    if post['user_id'] == current_user['user_id']:
                        if st.button("🗑️", key=f"del_{post['post_id']}", help="삭제"):
                            if post_mgr.delete_post(post['post_id'], current_user['user_id']):
                                st.success("삭제되었습니다!")
                                st.rerun()

                with btn_cols[3]:
                    if post['user_id'] != current_user['user_id']:
                        if st.button("🔁", key=f"retweet_{post['post_id']}", help="리트윗"):
                            if post_mgr.retweet_post(current_user['user_id'], post['post_id']):
                                st.success("리트윗되었습니다! 🔁")
                            else:
                                st.info("이미 리트윗한 글입니다.")
                            st.rerun()




        st.divider()



def show_write_page(current_user, post_mgr):
    """글쓰기 페이지"""
    st.header("✍️ 새 프롬프트 작성")

    st.markdown("💡 **다른 사람들이 실제로 사용할 수 있는 프롬프트를 공유해보세요!**")

    # 글쓰기 폼
    with st.form("write_form", clear_on_submit=True):
        content = st.text_area(
            "프롬프트 내용",
            placeholder="어떤 상황에서 사용하는 프롬프트인지, 어떻게 사용하는지 자세히 설명해주세요...",
            height=200
        )

        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submitted = st.form_submit_button("🚀 게시하기", type="primary")

        if submitted:
            if content.strip():
                success = post_mgr.create_post(current_user['user_id'], content.strip())

                if success:
                    st.success("프롬프트가 게시되었습니다! 🎉")
                    st.balloons()
                    import time
                    time.sleep(1.5)  # 1.5초 잠시 멈춤
                    st.session_state.menu = "🏠 홈"
                    st.rerun()
                else:
                    st.error("게시 중 오류가 발생했습니다.")
            else:
                st.error("내용을 입력해주세요!")

    st.divider()

    # 프롬프트 작성 가이드
    with st.expander("📝 좋은 프롬프트 작성 팁"):
        st.markdown("""
        **효과적인 프롬프트 작성법:**

        1. **구체적으로 작성하기**
        ```
        ❌ "코딩 도와줘"
        ✅ "파이썬으로 웹 크롤링 코드를 작성해주세요. 에러 처리와 주석도 포함해주세요."
        ```

        2. **사용 상황 설명하기**
        ```
        ✅ "ChatGPT에게 번역을 요청할 때 이 프롬프트를 사용하면 더 자연스러운 번역을 받을 수 있어요."
        ```

        3. **예시 포함하기**
        ```
        ✅ "예시: '안녕하세요'를 영어로 번역해주세요 → Hello! (친근한 인사)"
        ```
        """)



def show_profile_page(current_user, post_mgr, user_mgr):
    """프로필 페이지"""
    st.header("👤 내 프로필")
    
    # 사용자 정보 표시
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("https://images.unsplash.com/photo-1743449661678-c22cd73b338a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxmZWF0dXJlZC1waG90b3MtZmVlZHwzfHx8fHx8", width=100)
    
    with col2:
        st.subheader(f"**{current_user['user_name']}**")
        st.caption(f"가입일: {current_user['created_at']}")
    
    st.divider()

    # 내가 쓴 글 목록
    st.subheader("📝 내가 작성한 프롬프트")

    posts_with_likes = post_mgr.get_posts_with_likes()
    
    if len(posts_with_likes) == 0:
        st.info("📝 아직 작성한 프롬프트가 없습니다.")
        if st.button("✍️ 첫 프롬프트 작성하기"):
            st.session_state.menu = "✍️ 글쓰기"
            st.rerun()
        return
    
    # 사용자 이름 가져오기 위해 users와 조인 (홈페이지와 동일한 방식)
    users_df = user_mgr.load_users()
    posts_display = posts_with_likes.merge(
        users_df[['user_id', 'user_name']],
        on='user_id',
        how='left'
    )
    
    # 내가 쓴 글만 필터링
    my_posts = posts_display[posts_display['user_id'] == current_user['user_id']]

    if len(my_posts) > 0:
        st.info(f"총 {len(my_posts)}개의 프롬프트를 작성했습니다.")

        for idx, post in my_posts.iterrows():
            with st.container():
                col1, col2 = st.columns([8, 4])

                with col1:
                    # 내용 미리보기 (100자)
                    preview = post['content'][:100] + "..." if len(post['content']) > 100 else post['content']
                    st.markdown(f"**{preview}**")
                    
                    # NaN 값 체크 및 안전한 시간 문자열 처리
                    time_stamp = post['time_stamp']
                    if pd.isna(time_stamp):
                        time_display = "시간 정보 없음"
                    else:
                        try:
                            time_display = str(time_stamp)
                        except (AttributeError, IndexError):
                            time_display = "시간 정보 오류"
                    
                    st.caption(f"작성: {time_display} • 좋아요: {int(post['like_count'])}개")

                with col2:
                    if st.button("🗑️ 삭제", key=f"profile_del_{post['post_id']}"):
                        if post_mgr.delete_post(post['post_id'], current_user['user_id']):
                            st.success("삭제되었습니다!")
                            st.rerun()

            st.divider()
    else:
        st.info("📝 아직 작성한 프롬프트가 없습니다.")
        if st.button("✍️ 첫 프롬프트 작성하기"):
            st.session_state.menu = "✍️ 글쓰기"
            st.rerun()


# 매니저 초기화
@st.cache_resource
def init_managers():
    try:
        user_mgr = UserManager()
        post_mgr = PostManager()
        return user_mgr, post_mgr
    except Exception as e:
        st.error(f"매니저 초기화 중 오류가 발생했습니다: {str(e)}")
        return None, None

user_mgr, post_mgr = init_managers()

# 매니저 초기화 확인
if user_mgr is None or post_mgr is None:
    st.error("⚠️ 시스템 초기화에 실패했습니다. 페이지를 새로고침해주세요.")
    st.stop()


# --- 세션 기본값 ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'menu' not in st.session_state:
    st.session_state.menu = "🏠 홈"

if 'editing_post' not in st.session_state:
    st.session_state.editing_post = None

if not st.session_state.logged_in :
    # 로그인 하지 않은 경우
    show_auth_page()
    st.stop()

else: 
    #로그인한 경우 
    current_user = st.session_state.current_user    

    st.title('🦄 개발 유니콘다')
    st.write(f'**{current_user["user_name"]}님 환영합니다**')


    if st.sidebar.button("🚪 로그아웃", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun() 

    st.sidebar.title("📋 메뉴")

    menu = st.sidebar.selectbox(
    "선택하세요",
    ["🏠 홈", "✍️ 글쓰기", "👤 프로필",'📊 데이터 확인'],
    index=["🏠 홈", "✍️ 글쓰기", "👤 프로필",'📊 데이터 확인'].index(st.session_state.menu)
    )

        # 메뉴 변경 감지
    if menu != st.session_state.menu:
        st.session_state.menu = menu
        st.rerun()


    # 페이지 표시
    if menu == "🏠 홈":
        show_home_page(current_user, post_mgr, user_mgr)
    elif menu == "✍️ 글쓰기":
        show_write_page(current_user, post_mgr)
    elif menu == "👤 프로필":
        show_profile_page(current_user, post_mgr, user_mgr)








    # if menu == "🏠 홈" :
    #     st.header('📝 최근 뉴스')

    #     # 샘플 게시글 (3단계에서 실제 데이터로 교체)
    #     st.info("💡 3단계에서 실제 게시글 기능이 구현됩니다!")

    #     with st.container() :
    #         col1, col2 = st.columns([1, 10])
    #         with col1:
    #             st.image("https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=50&h=50&fit=crop&crop=face", width=50)
    #         with col2:
    #             st.markdown(f"**{current_user['user_name']}** • 방금 전")
    #             st.markdown("로그인 시스템이 완성되었습니다! 🎉")
    #             st.button("❤️ 0", key="sample_like")

        

    # elif menu == "✍️ 글쓰기":
    #     st.header("✍️ 새 프롬프트 작성")
    #     st.info("💡 3단계에서 실제 글쓰기 기능이 구현됩니다!")

    #     content = st.text_area("프롬프트 내용", height=150)
    #     if st.button("게시하기", type="primary"):
    #         if content:
    #             st.success("3단계에서 실제 저장 기능이 추가됩니다! 🎉")
    #         else:
    #             st.error("내용을 입력해주세요.")

    # elif menu == "👤 프로필":
    #     st.header("👤 내 프로필")

    #     col1, col2 = st.columns([1, 3])
    #     with col1:
    #         st.image("https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face", width=100)

    #     with col2:
    #         st.markdown(f"### {current_user['username']}")
    #         st.markdown(f"**사용자 ID:** {current_user['user_id']}")
    #         st.markdown(f"**가입일:** {current_user['created_at']}")

    #     st.divider()

    #     # 활동 통계 (더미 데이터)
    #     col1, col2, col3 = st.columns(3)
    #     with col1:
    #         st.metric("작성한 글", "0")
    #     with col2:
    #         st.metric("받은 좋아요", "0")
    #     with col3:
    #         st.metric("활동일", "1")

    # elif menu == "📊 데이터 확인":
    #     st.header("📊 저장된 데이터 확인")

    #     user_mgr = UserManager()
    #     users_df = user_mgr.load_users()

    #     st.subheader("👥 사용자 목록")

    #     if len(users_df) > 0:
    #         # 비밀번호 숨기기
    #         display_df = users_df.copy()
    #         display_df['password'] = '***'
    #         st.dataframe(display_df, use_container_width=True)

    #         # 간단한 통계
    #         col1, col2 = st.columns(2)
    #         with col1:
    #             st.metric("총 사용자 수", len(users_df))
    #         with col2:
    #             today_users = len(users_df[users_df['created_at'] == current_user['created_at']])
    #             st.metric("오늘 가입자", today_users)
    #     else:
    #         st.warning("등록된 사용자가 없습니다.")

