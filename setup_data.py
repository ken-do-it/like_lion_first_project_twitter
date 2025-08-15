import pandas as pd
import os 

csv_args = {'index':False, 'encoding':'utf=8'}

def create_data_folder() :
    """data 폴더와 초기 CSV 파일들 생성"""
    # data 폴더 생성
    if not os.path.exists('data') :
        os.makedirs('data')
        print("📁 data 폴더가 생성되었습니다.")

    # 빈 users.csv 파일 생성
    if not os.path.exists('data/users.csv'):
        users_columns = ['user_id', 'user_name', 'password', 'created_at']
        empty_users= pd.DataFrame(columns=users_columns)
        empty_users.to_csv('data/users.csv', **csv_args)
        print("📄 data/users.csv 파일이 생성되었습니다.")
    
    # 빈 posts.csv 파일 생성 (3단계용)
    if not os.path.exists('data/posts.csv') :
        posts_columns= ['post_id', 'user_id', 'content', 'time_stamp']
        empty_posts = pd.DataFrame(columns=posts_columns)
        empty_posts.to_csv('data/posts.csv', **csv_args)
        print("📄 data/posts.csv 파일이 생성되었습니다.")
    # 빈 likes.csv 파일 생성 (3단계용)
    if not os.path.exists('data/likes.csv') :
        likes_columns = ['like_id', 'user_id', 'post_id', 'time_stamp']
        empty_likes = pd.DataFrame(columns=likes_columns)
        empty_likes.to_csv('data/likes.csv', **csv_args)
        print("📄 data/likes.csv 파일이 생성되었습니다.")
    # 빈 re_twit.csv 파일 생성 (3단계용)
    if not os.path.exists('data/re_twits.csv') :
        re_twits_columns = ['re_twit_id', 'user_id', 'post_id', 'time_stamp']
        empty_re_twits = pd.DataFrame(columns=re_twits_columns)
        empty_re_twits.to_csv('data/re_twits.csv', **csv_args)
        print("📄 data/re_twits.csv 파일이 생성되었습니다.")
    print("✅ 초기 설정이 완료되었습니다!")

if __name__ == '__main__' :
    create_data_folder()