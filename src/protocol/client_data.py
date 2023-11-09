import random
from dataclasses import dataclass, field
import socket
from typing import ClassVar

from colour import Color


@dataclass
class ServerClientData:
    conn: socket.socket = field(repr=False)
    addr: tuple
    username: str
    color: str

@dataclass
class ClientClientData:
    username: str
    color: str



