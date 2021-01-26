class ErrorCode:
    ERR_STUDENT_HAS_TEAM = 0
    INCORRECT_PASSWORD = 1
    IS_TEAM_ADMIN = 3
    TOO_MANY_TEAMS = 4
    HAS_MEMBERS = 5
    TOO_MANY_MEMBERS = 6
    HAS_NO_TEAM = 7

    NOT_EXISTS_MESSAGE = 101
    NOT_EXISTS_STUDENT = 102
    NOT_EXISTS_TEACHER = 103
    NOT_EXISTS_TEAM = 104
    NOT_EXISTS_USER = 105


class MessageInfo:
    NOT_EXISTS_MESSAGE = "Nie ma takiej wiadomości"
    NOT_EXISTS_STUDENT = "Taki student nie istnieje"
    NOT_EXISTS_TEACHER = "Taki prowadzący nie istnieje"
    NOT_EXISTS_TEAM = "Taki zespół nie istnieje"
    NOT_EXISTS_USER = "Użytkownik nie istnieje"

    HAS_TEAM = "Student ma już zespół"
    HAS_NO_TEAM = "Student nie ma zespołu"
    IS_TEAM_ADMIN = "Admin nie może opuścić zespołu"
    TOO_MANY_TEAMS = "Opiekun ma już 3 zespoły"
    HAS_MEMBERS = "Nie można wykonać - zespół na członków"
    TOO_MANY_MEMBERS = "Zespół ma już 4 członków"

    INCORRECT_PASSWORD = "Niewłaściwe hasło"

    SUBJ_INVITATION = "Rozpatrzenie zaproszenie"
    MSG_INVITATION_ACCEPT = "Użytkownik zaakceptował zaproszenie"
    MSG_INVITATION_REFUSE = "Użytkownik odrzucił zaproszenie"
