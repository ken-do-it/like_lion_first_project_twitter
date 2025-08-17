# post_manager.py
import pandas as pd
import os
import uuid
from datetime import datetime

class PostManager:
    def __init__(self):
        self.posts_path = 'data/posts.csv'
        self.likes_path = 'data/likes.csv'
        self.setup_files()

    def setup_files(self):
        """CSV 파일이 없으면 생성"""
        os.makedirs('data', exist_ok=True)

        # posts.csv 생성
        if not os.path.exists(self.posts_path):
            posts_df = pd.DataFrame(columns=['post_id', 'user_id', 'content', 'time_stamp', 'is_retweet', 'original_post_id'])
            posts_df.to_csv(self.posts_path, index=False, encoding='utf-8')

        # likes.csv 생성
        if not os.path.exists(self.likes_path):
            likes_df = pd.DataFrame(columns=['like_id', 'user_id', 'post_id', 'time_stamp'])
            likes_df.to_csv(self.likes_path, index=False, encoding='utf-8')

    def load_posts(self):
        """게시글 데이터 불러오기"""
        posts_df = pd.read_csv(self.posts_path, encoding='utf-8')
        
        # 기존 데이터와의 호환성을 위해 timestamp 컬럼을 time_stamp로 통일
        if 'timestamp' in posts_df.columns and 'time_stamp' in posts_df.columns:
            # 두 컬럼이 모두 있는 경우, timestamp의 값을 time_stamp로 복사
            posts_df['time_stamp'] = posts_df['timestamp'].fillna(posts_df['time_stamp'])
            posts_df = posts_df.drop('timestamp', axis=1)
        elif 'timestamp' in posts_df.columns and 'time_stamp' not in posts_df.columns:
            # timestamp만 있는 경우, time_stamp로 이름 변경
            posts_df['time_stamp'] = posts_df['timestamp']
            posts_df = posts_df.drop('timestamp', axis=1)
        
        # NaN 값이 있는 경우 기본값으로 설정
        posts_df['time_stamp'] = posts_df['time_stamp'].fillna('2025-01-01 00:00:00')
        
        # 새로운 리트윗 컬럼들이 없는 경우 추가
        if 'is_retweet' not in posts_df.columns:
            posts_df['is_retweet'] = False
        if 'original_post_id' not in posts_df.columns:
            posts_df['original_post_id'] = None
        
        return posts_df

    def load_likes(self):
        """좋아요 데이터 불러오기"""
        return pd.read_csv(self.likes_path, encoding='utf-8')

    def save_posts(self, df):
        """게시글 데이터 저장"""
        df.to_csv(self.posts_path, index=False, encoding='utf-8')

    def save_likes(self, df):
        """좋아요 데이터 저장"""
        df.to_csv(self.likes_path, index=False, encoding='utf-8')

    def create_post(self, user_id, content, is_retweet=False, original_post_id=None):
        """새 게시글 작성 (리트윗 포함)"""
        posts_df = self.load_posts()

        new_post = {
            'post_id': str(uuid.uuid4())[:8],
            'user_id': user_id,
            'content': content,
            'time_stamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_retweet': is_retweet,
            'original_post_id': original_post_id if is_retweet else None
        }

        # 새 글을 맨 위에 추가
        new_row = pd.DataFrame([new_post])
        posts_df = pd.concat([new_row, posts_df], ignore_index=True)

        self.save_posts(posts_df)
        return True

    def retweet_post(self, user_id, original_post_id):
        """Retweet a post, showing the original post's username in the content."""
        posts_df = self.load_posts()

        # Find the original post
        original_post = posts_df[posts_df['post_id'] == original_post_id]
        if len(original_post) == 0:
            return False

        # Prevent duplicate retweets
        existing_retweet = posts_df[
            (posts_df['user_id'] == user_id) &
            (posts_df['original_post_id'] == original_post_id)
        ]
        if len(existing_retweet) > 0:
            return False

        # Get original user_id and content
        original_user_id = original_post.iloc[0]['user_id']
        original_content = original_post.iloc[0]['content']

        # Get original username from users.csv
        try:
            users_df = pd.read_csv('data/users.csv', encoding='utf-8')
            user_row = users_df[users_df['user_id'] == original_user_id]
            if len(user_row) > 0:
                original_username = user_row.iloc[0]['user_name']
            else:
                original_username = original_user_id
        except Exception:
            original_username = original_user_id

        # Compose retweet content
        retweet_content = f"🔁 리트윗: {original_username}\n{original_content}"

        return self.create_post(user_id, retweet_content, True, original_post_id)

    def update_post(self, post_id, user_id, new_content):
        """게시글 수정 (작성자만 가능)"""
        posts_df = self.load_posts()

        # 작성자인지 확인
        post = posts_df[
            (posts_df['post_id'] == post_id) &
            (posts_df['user_id'] == user_id)
        ]

        if len(post) == 0:
            return False

        # 게시글 수정
        posts_df.loc[posts_df['post_id'] == post_id, 'content'] = new_content
        posts_df.loc[posts_df['post_id'] == post_id, 'time_stamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.save_posts(posts_df)
        return True

    def get_posts_with_likes(self):
        """게시글과 좋아요 수를 합쳐서 반환"""
        posts_df = self.load_posts()
        likes_df = self.load_likes()

        if len(posts_df) == 0:
            return pd.DataFrame()

        # 각 게시글별 좋아요 수 계산
        if len(likes_df) > 0:
            like_counts = likes_df.groupby('post_id').size().reset_index(name='like_count')
            # posts와 like_counts 조인
            result = posts_df.merge(like_counts, on='post_id', how='left')
        else:
            result = posts_df.copy()
            result['like_count'] = 0

        result['like_count'] = result['like_count'].fillna(0).astype(int)
        return result

    def toggle_like(self, user_id, post_id):
        """좋아요 토글 (있으면 취소, 없으면 추가)"""
        likes_df = self.load_likes()

        # 이미 좋아요했는지 확인
        existing = likes_df[
            (likes_df['user_id'] == user_id) &
            (likes_df['post_id'] == post_id)
        ]

        if len(existing) > 0:
            # 좋아요 취소
            likes_df = likes_df[~(
                (likes_df['user_id'] == user_id) &
                (likes_df['post_id'] == post_id)
            )]
            self.save_likes(likes_df)
            return False  # 취소됨
        else:
            # 좋아요 추가
            new_like = {
                'like_id': str(uuid.uuid4())[:8],
                'user_id': user_id,
                'post_id': post_id,
                'time_stamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            new_row = pd.DataFrame([new_like])
            likes_df = pd.concat([likes_df, new_row], ignore_index=True)
            self.save_likes(likes_df)
            return True  # 추가됨

    def is_liked_by_user(self, user_id, post_id):
        """특정 사용자가 좋아요했는지 확인"""
        likes_df = self.load_likes()
        liked = likes_df[
            (likes_df['user_id'] == user_id) &
            (likes_df['post_id'] == post_id)
        ]
        return len(liked) > 0

    def delete_post(self, post_id, user_id):
        """게시글 삭제 (작성자만 가능)"""
        posts_df = self.load_posts()

        # 작성자인지 확인
        post = posts_df[
            (posts_df['post_id'] == post_id) &
            (posts_df['user_id'] == user_id)
        ]

        if len(post) == 0:
            return False

        # 게시글 삭제
        posts_df = posts_df[posts_df['post_id'] != post_id]
        self.save_posts(posts_df)

        # 관련 좋아요도 삭제
        likes_df = self.load_likes()
        likes_df = likes_df[likes_df['post_id'] != post_id]
        self.save_likes(likes_df)

        return True

