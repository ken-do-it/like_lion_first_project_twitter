# skills_manager.py
# skills_manager.py
import os
import uuid
from datetime import datetime
import pandas as pd

class SkillsManager:
    def __init__(self, csv_path: str = "data/my_skills.csv"):
        self.csv_path = csv_path
        self.columns = [
            "skill_id",     # uuid 짧게
            "user_id",
            "user_name",
            "skill_name",
            "level",        # 0~100 정수
            "created_at",
            "updated_at",
        ]
        self._ensure_csv()

    # ---------- 내부 유틸 ----------
    def _ensure_csv(self):
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        if not os.path.exists(self.csv_path):
            pd.DataFrame(columns=self.columns).to_csv(self.csv_path, index=False, encoding="utf-8")

    def _load(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.csv_path, encoding="utf-8")
        except Exception:
            df = pd.DataFrame(columns=self.columns)
        # 누락 컬럼 보정
        for c in self.columns:
            if c not in df.columns:
                df[c] = None
        # 타입 보정
        if "level" in df.columns:
            df["level"] = pd.to_numeric(df["level"], errors="coerce").fillna(0).astype(int)
        return df[self.columns].copy()

    def _save(self, df: pd.DataFrame):
        df[self.columns].to_csv(self.csv_path, index=False, encoding="utf-8")

    # ---------- 공개 API ----------
    def add_skill(self, user_id: str, user_name: str, skill_name: str, level: int) -> str:
        """
        스킬 추가. 성공 시 생성된 skill_id 반환
        """
        df = self._load()
        sid = str(uuid.uuid4())[:8]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = {
            "skill_id": sid,
            "user_id": user_id,
            "user_name": user_name,
            "skill_name": skill_name,
            "level": int(level),
            "created_at": now,
            "updated_at": now,
        }
        df = pd.concat([pd.DataFrame([new_row]), df], ignore_index=True)
        self._save(df)
        return sid

    def list_user_skills(self, user_id: str) -> pd.DataFrame:
        """
        해당 사용자의 스킬 목록 DataFrame 반환 (skill_id, user_id, user_name, skill_name, level, created_at, updated_at)
        """
        df = self._load()
        rows = df[df["user_id"] == user_id].copy()
        # 최신순 정렬
        if "updated_at" in rows.columns:
            rows = rows.sort_values("updated_at", ascending=False)
        return rows.reset_index(drop=True)

    def rename_skill(self, skill_id: str, new_name: str) -> bool:
        """
        스킬명 변경
        """
        if not new_name.strip():
            return False
        df = self._load()
        idx = df.index[df["skill_id"] == skill_id]
        if len(idx) == 0:
            return False
        df.loc[idx, "skill_name"] = new_name.strip()
        df.loc[idx, "updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save(df)
        return True

    def update_skill_level(self, skill_id: str, new_level: int) -> bool:
        """
        숙련도 변경 (0~100)
        """
        new_level = max(0, min(100, int(new_level)))
        df = self._load()
        idx = df.index[df["skill_id"] == skill_id]
        if len(idx) == 0:
            return False
        df.loc[idx, "level"] = new_level
        df.loc[idx, "updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save(df)
        return True

    def delete_skill(self, skill_id: str) -> bool:
        """
        스킬 삭제
        """
        df = self._load()
        before = len(df)
        df = df[df["skill_id"] != skill_id]
        if len(df) == before:
            return False
        self._save(df)
        return True
