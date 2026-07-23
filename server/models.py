from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class ChatMessage:
    channel: str
    login: str
    display_name: str
    text: str
    color: str
    emotes: list[dict] = field(default_factory=list)

    badges: List[dict] = field(default_factory=list)

    department: str = "Общий"
    department_color: str = "#5fc95f"

    speech: str = "говорит"

    loud_voice: bool = False

    def to_dict(self) -> dict:
        return {
            "channel": self.channel,
            "login": self.login,
            "display_name": self.display_name,
            "text": self.text,
            "color": self.color,
            "badges": self.badges,
            "department": self.department,
            "department_color": self.department_color,
            "speech": self.speech,
            "loud_voice": self.loud_voice,
            "emotes": self.emotes,
        }