import streamlit as st
from user_manager import UserManager


def show_auth_page() :
        
    st.title('🦄 유니콘다에 오신걸 환영합니다')
    st.write('여기는 개발에 관련한 모든것을 소통하는 곳 입니다')

    with st.container() :
        st.subheader('로그인')
        st.write('로그인 후 서비스를 이용해주세요, 계정이 없으시면 회원가입을 해주세요')

        # # 로그인 폼
        # st.text_input('아이디를 입력해주세요', key='user_id')
        # st.text_input('패스워드를 입력해주세요', type='password', key='user_pw')

        tab1, tab2 = st.tabs(["🔑 로그인", "📝 회원가입"])

        user_mgr = UserManager()

        with tab1 :
            st.subheader("로그인")

            user_name = st.text_input("사용자 아이디" , key='login_user_name')
            password = st.text_input('비밀번호', type='password', key='login_password')

            if st.button('로그인', type='primary') :
                if user_name and password :
                    success, user_info = user_mgr.login_user(user_name, password)

                    if success :
                        # session state 에 로그인 정보 저장
                        st.session_state.logged_in = True
                        st.session_state.current_user =user_info
                        st.success(f'✅ {user_name}님 환영합니다!')
                        st.rerun()
                    else :
                        st.error('❌ 사용자명 또는 비밀번호가 틀렸습니다.')
                else:
                    st.warning('⚠️ 모든 필드를 입력해주세요.')
        with tab2 :
            st.subheader("회원가입")
            new_user_name = st.text_input("사용자 아이디", key='signUp_user_name')
            new_password = st.text_input('비밀번호', type='password', key='signUp_password')
            confirm_password = st.text_input('비밀번호 확인', type='password')

            if st.button('회원가입', type='primary') :
                if new_user_name and new_password and confirm_password :
                    if new_password == confirm_password :
                        success, message = user_mgr.create_user(new_user_name, new_password)

                        if success :
                            st.success(f"🎉 {message}")
                            st.info('💡 이제 로그인 탭에서 로그인해보세요!')
                        else :
                            st.error(f"❌  {message}")
                    else :
                        st.error("❌ 비밀번호가 일치하지 않습니다.")
                else :
                    st.warning('⚠️ 모든 필드를 입력해주세요.')
                
        # 현재 가입자 수 표시 
        st.sidebar.metric("📊 총 가입자 수", user_mgr.get_user_count())    

def logout_user() :
    """로그아웃 처리"""
    st.session_state.logged_in = False
    if 'current_user' in st.session_state :
        del st.session_state.current_user
    st.rerun()

