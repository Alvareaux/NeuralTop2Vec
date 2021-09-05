
class LangNeural:

    def get_lang(self, text: str, lang_count: int = 1) -> str:
        raise NotImplementedError

    def get_lang_prob(self, text: str, lang_count: int = 1) -> list[str]:
        raise NotImplementedError
