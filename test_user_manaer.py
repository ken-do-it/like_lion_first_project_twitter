# test_user_manager.py
from user_manager import UserManager

# 테스트 실행
user_mgr = UserManager()

print("📊 현재 사용자 수:", user_mgr.get_user_count())

# 회원가입 테스트
success, message = user_mgr.create_user("lion", "123")
print("회원가입 결과:", message)

# 로그인 테스트
success, user_info = user_mgr.login_user("lion", "123")
if success:
    print(f"✅ 로그인 성공: {user_info}")
else:
    print("❌ 로그인 실패")

