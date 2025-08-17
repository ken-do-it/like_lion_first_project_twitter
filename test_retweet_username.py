import pandas as pd
from post_manager import PostManager

def test_retweet_shows_original_username():
    # 테스트용 users.csv 생성
    users = pd.DataFrame([
        {'user_id': 'user_001', 'user_name': '테스트러', 'password': 'pw', 'created_at': '2025-08-15', 'profile_image': ''},
        {'user_id': 'user_002', 'user_name': 'lion', 'password': 'pw', 'created_at': '2025-08-15', 'profile_image': ''}
    ])
    users.to_csv('data/users.csv', index=False, encoding='utf-8')

    # 테스트용 posts.csv 초기화
    posts = pd.DataFrame([
        {'post_id': 'post_abc', 'user_id': 'user_002', 'content': '원본 내용입니다', 'time_stamp': '2025-08-17 13:00:00', 'is_retweet': False, 'original_post_id': None}
    ])
    posts.to_csv('data/posts.csv', index=False, encoding='utf-8')

    # PostManager 인스턴스 생성
    pm = PostManager()

    # user_001이 post_abc를 리트윗
    pm.retweet_post('user_001', 'post_abc')

    # 결과 확인
    posts_df = pd.read_csv('data/posts.csv', encoding='utf-8')
    retweet_row = posts_df[(posts_df['user_id'] == 'user_001') & (posts_df['is_retweet'] == True)]

    assert len(retweet_row) == 1, "리트윗이 생성되지 않았습니다."
    content = retweet_row.iloc[0]['content']
    print("리트윗 content:", content)
    assert "리트윗: lion" in content, "원래 포스트 유저 이름이 포함되어 있지 않습니다."
    assert "원본 내용입니다" in content, "원래 포스트 내용이 포함되어 있지 않습니다."
    print("테스트 통과!")

if __name__ == "__main__":
    test_retweet_shows_original_username()