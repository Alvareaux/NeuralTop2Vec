
class TopicEngine:

    def create_model(self, settings):
        raise NotImplementedError

    def load_model(self, path: str):
        raise NotImplementedError

    def save_model(self, path: str):
        raise NotImplementedError
