from app.common.enums import UserClass, UserStudy


class EnumUtils:
    @staticmethod
    def get_user_enums(**kwargs):
        try:
            user_class = UserClass(int(kwargs["user_class"]))
            user_study = UserStudy(int(kwargs["user_study"]))
            return user_class, user_study
        except Exception:
            return None, None
