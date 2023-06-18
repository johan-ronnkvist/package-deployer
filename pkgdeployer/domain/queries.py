from dataclasses import dataclass
from uuid import UUID


class Query:
    """Queries are used to retrieve information from the system. """
    pass


@dataclass(frozen=True)
class FindPackageQuery(Query):
    uuid: UUID
