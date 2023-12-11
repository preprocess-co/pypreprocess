import json

class PreprocessResponse:
    def __init__(self, data, status=None, error=None, success=None, message=None, info=None) -> None:
        self.data = data

        self.status = status
        self.error = error
        self.success = success
        self.message = message
        self.info = info

    def to_json(self) -> str:
       return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self) -> str:
        return self.to_json()
