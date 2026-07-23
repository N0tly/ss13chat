COMMON = ("Общий", "#5fc95f")
SECURITY = ("Безопасность", "#ff3232")
SUPPLY = ("Снабжение", "#b78740")
MEDICAL = ("Медицина", "#00b9f2")
COMMAND = ("Командование", "#ffe000")


def get_role(badges: list[dict]) -> tuple[str, str, bool]:

    names = {
        badge["name"]
        for badge in badges
    }

    if "bot-badge" in names:
        return (*MEDICAL, False)

    if "broadcaster" in names:
        return (*COMMAND, True)

    if "vip" in names:
        return (*COMMAND, True)

    if "moderator" in names:
        return (*SECURITY, False)

    if "subscriber" in names:
        return (*SUPPLY, False)

    return (*COMMON, False)