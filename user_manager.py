import pandas as pd
import os
from datetime import datetime

class UserManager:
    def __init__(self) :
        self.csv_path = 'data/users.csv'
        self.csv_args = {'index':False, 'encoding':'utf-8'}
        self.users_columns = ['user_id', 'user_name', 'password', 'created_at', 'profile_image']
        self.ensure_csv_exists()


    def ensure_csv_exists(self) :
        """CSV 파일이 없으면 생성"""

        if not os.path.exists(self.csv_path) :
            os.makedirs('data', exist_ok=True)
            empty_info = pd.DataFrame(columns=self.users_columns)
            empty_info.to_csv(self.csv_path, **self.csv_args)

    def load_users(self) :
        ''' 사용자 데이터 불러오기'''

        try:
            return pd.read_csv(self.csv_path, encoding='utf-8')
        except:
            return pd.DataFrame(columns=self.users_columns)
        
    def save_users(self, user_info):
        """사용자 데이터 저장"""

        user_info.to_csv(self.csv_path, index=False, encoding='utf-8')
        
    
    def create_user(self, user_name, password) :
        """새 사용자 생성"""

        users_info = self.load_users()

        # 중복 사용자명 체크
        if user_name in users_info["user_name"].values:
            return False, "이미 존재하는 사용자명입니다"
        
        # 새 사용자 ID 생성
        users_count = len(users_info)
        new_user_id = f"user_{users_count +1:03d}"

        # 기본 프로필 이미지 설정 (랜덤하게 선택)
        default_images = [
            "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face"
        ]
        import random
        default_profile_image = random.choice(default_images)

        # 새 사용자 데이터
        new_user = {
            'user_id': new_user_id,
            'user_name': user_name,
            'password': password,
            'created_at': datetime.now().strftime('%Y-%m-%d'),
            'profile_image': default_profile_image
        }

        # DataFrame에 추가
        new_row = pd.DataFrame([new_user])
        users_info = pd.concat([users_info, new_row], ignore_index=True)

        # 저장
        self.save_users(users_info)
        return True, "회원가입이 완료되었습니다."

    def login_user(self, user_name, password) :
        """사용자 로그인 검증"""
        user_info = self.load_users()
        username = str(user_name).strip()
        password = str(password).strip()

        #사용자 찾기 
        user_data = user_info [
            (user_info['user_name'] == username) &
            (user_info['password'] == password)
        ]

        if len(user_data) == 1:
            user_info =user_data.iloc[0].to_dict()
            return True, user_info
        else :
            return False, None
    
    def get_user_count(self) :
        """총 사용자 수 반환"""
        user_info = self.load_users()
        return len(user_info)

    def get_user_profile_image(self, user_id):
        """사용자의 프로필 이미지 URL 반환"""
        users_info = self.load_users()
        user_data = users_info[users_info['user_id'] == user_id]
        
        if len(user_data) > 0:
            profile_image = user_data.iloc[0]['profile_image']
            # NaN 체크 및 기본 이미지 반환
            if pd.isna(profile_image) or not profile_image:
                return "https://images.unsplash.com/photo-1743449661678-c22cd73b338a?w=150&h=150&fit=crop&q=60"
            return profile_image
        return "https://images.unsplash.com/photo-1743449661678-c22cd73b338a?w=150&h=150&fit=crop&q=60"

    def update_profile_image(self, user_id, new_image_url):
        """사용자의 프로필 이미지 업데이트"""
        users_info = self.load_users()
        user_idx = users_info[users_info['user_id'] == user_id].index
        
        if len(user_idx) > 0:
            users_info.loc[user_idx[0], 'profile_image'] = new_image_url
            self.save_users(users_info)
            return True
        return False

    def get_available_profile_images(self):
        """사용 가능한 프로필 이미지 목록 반환"""
        return [
            "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150&h=150&fit=crop&crop=face"
        ]



