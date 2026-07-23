from config import DEFAULT_NICK_COLOR

from server.models import ChatMessage
from server.roles import get_role
from server.speech import get_speech


def parse(channel: str, raw: str) -> ChatMessage | None:

    if "PRIVMSG" not in raw:
        return None

    try:

        tags_raw, payload = raw.split(" PRIVMSG ", 1)

        message = (
            payload.split(" :", 1)[1]
            .rstrip(
                " \t\r\n\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u202F\u205F\u3000\u200B\u200C\u200D\u2060\uFEFF")
        )

        tags = {}

        for pair in tags_raw[1:].split(";"):
            if "=" not in pair:
                continue

            key, value = pair.split("=", 1)

            tags[key] = value

        login = tags.get("login", "")

        display = tags.get("display-name") or login

        color = tags.get("color") or DEFAULT_NICK_COLOR

        badges = []

        badges_raw = tags.get("badges", "")

        if badges_raw:
            badges = [
                badge.split("/")[0]
                for badge in badges_raw.split(",")
            ]

        department, department_color, loud_voice = get_role(badges)
        # print(login, badges)
        return ChatMessage(
            channel=channel,
            login=login,
            display_name=display,
            text=message,
            color=color,
            badges=badges,
            department=department,
            department_color=department_color,
            speech=get_speech(message),
            loud_voice=loud_voice,
        )

    except Exception:
        return None