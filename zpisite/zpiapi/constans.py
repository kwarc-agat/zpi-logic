
class ErrorCode:
    ERR_STUDENT_HAS_TEAM = 0,
    INCORRECT_PASSWORD = 1
    IS_TEAM_ADMIN = 3
    TOO_MANY_TEAMS = 4
    HAS_MEMBERS = 5
    TOO_MANY_MEMBERS = 6
    HAS_TEAM = 7

    NOT_EXISTS_MESSAGE = 101
    NOT_EXISTS_STUDENT = 102
    NOT_EXISTS_TEACHER = 103
    NOT_EXISTS_TEAM = 104
    NOT_EXISTS_USER = 105



class MessageInfo:
    NOT_EXISTS_MESSAGE = "Message does not exist"
    NOT_EXISTS_STUDENT = "Student does not exist"
    NOT_EXISTS_TEACHER = "Teacher does not exist"
    NOT_EXISTS_TEAM = "Team does not exist"
    NOT_EXISTS_USER = "User does not exist"

    HAS_TEAM = "Student has team"
    HAS_NO_TEAM = "Student does not have team"
    IS_TEAM_ADMIN = "Team admin cannot leave"
    TOO_MANY_TEAMS = "Lecturer has 3 teams already"
    HAS_MEMBERS = "Team has multiple members"
    TOO_MANY_MEMBERS = "Team has 4 members already"

    INCORRECT_PASSWORD = "Wrong password"

    SUBJ_INVITATION = "Rozpatrzenie zaproszenie"
    MSG_INVITATION_ACCEPT = "Użytkownik zaakceptował zaproszenie"
    MSG_INVITATION_REFUSE = "Użytkownik odrzucił zaproszenie"

