import pandas as pd
import os
from datetime import datetime

class UserManager:
    def __init__(self) :
        self.csv_path = 'data/users.csv'
        self.csv_args = {'index':False, 'encoding':'utf=8'}
        self.users_columns = ['user_id', 'user_name', 'password', 'created_at']
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

        # 새 사용자 데이터
        new_user = {
            'user_id': new_user_id,
            'user_name': user_name,
            'password': password,
            'created_at': datetime.now().strftime('%Y-%m-%d')
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

        #사용자 찾기 
        user_data = user_info [
            (user_info['user_name'] == user_name) &
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



    # def ensure_csv_exists(self) :
    #     """CSV 파일이 없으면 생성"""

    #     if not os.path.exists(self.csv_path) :
    #         os.makedirs('data', exist_ok=True) # 만약 존재하면 error가 발생하기 때문에 True로 넘겨준다 이미 위에서 한번 검사했지만 다시 한번더 검사 
    #         empty_users_info = pd.DataFrame(columns=self.users_columns)
    #         empty_users_info.to_csv(self.csv_path, **self.csv_args)
    

    
    # def load_users(self) :
    #     ''' 사용자 데이터 로드'''

    #     try :
    #         return pd.read_csv(self.csv_path, encoding='utf-8')
    #     except: 
    #         return pd.DataFrame(columns=self.users_columns)
        
    


