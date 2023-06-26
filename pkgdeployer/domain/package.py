from uuid import UUID


class Package:
    def __init__(self, uuid: UUID, name: str):
        self._uuid = uuid
        self._name = name

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def name(self) -> str:
        return self._name

    def __hash__(self):
        return hash(self.uuid)

    def __eq__(self, other):
        return self.uuid == other.uuid and self.name == other.name
