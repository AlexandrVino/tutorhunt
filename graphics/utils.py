class CONST:
    WEEKDAYS = (
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    )
    WEEKDAYS_RUS = (
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
        "воскресенье"
    )
    HOURS = tuple(['%02d:00' % i for i in range(24)])
