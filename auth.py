import streamlit as st


def show_auth_page() :
        
    st.title('🦄 유니콘다에 오신걸 환영합니다')
    st.write('여기는 개발에 관련한 모든것을 소통하는 곳 입니다')

    with st.container() :
        st.subheader('로그인')
        st.write('로그인 후 서비스를 이용해주세요, 계정이 없으시면 회원가입을 해주세요')

        # 로그인 폼
        st.text_input('아이디를 입력해주세요', key='user_id')
        st.text_input('패스워드를 입력해주세요', type='password', key='user_pw')

        col1, col2 = st.columns(2)
        with col1:
            if st.button('로그인', type='primary') :
                # TODO: 여기에 실제 인증 로직을 넣고, 실패 시 메시지 표시
                st.session_state.logged_in = False
                st.rerun()
                # st.success('로그인 성공! 환영합니다.')
            else:
                st.error('로그인 실패! 아이디와 패스워드를 확인해주세요.')
        with col2:
            if st.button('회원가입', type='secondary') :
                st.info('회원가입 페이지로 이동합니다.')