COMMON = ("Общий", "#5fc95f")
SECURITY = ("Безопасность", "#ff3232")
SUPPLY = ("Снабжение", "#b78740")
MEDICAL = ("Медицина", "#00b9f2")
COMMAND = ("Командование", "#ffe000")


def get_role(badges: list[str]) -> tuple[str, str, bool]:
    badges = set(badges)
    if "bot-badge" in badges:
        return (*MEDICAL, False)

    if "broadcaster" in badges:
        return (*COMMAND, True)

    if "vip" in badges:
        return (*COMMAND, True)

    if "moderator" in badges:
        return (*SECURITY, False)

    if "subscriber" in badges:
        return (*SUPPLY, False)

    return (*COMMON, False)