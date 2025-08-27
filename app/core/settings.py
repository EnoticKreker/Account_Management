from uuid import UUID


class AppState:
    def __init__(self):
        self.users: dict[UUID, dict] = {}
        self.users_list: list = []


app_state = AppState()
