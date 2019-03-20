import reminders

CALENDAR = "Overcast"


class Reminders:
    def __init__(self):
        all_calendars = reminders.get_all_calendars()
        for calendar in all_calendars:
            if calendar.title == CALENDAR:
                self.calendar = calendar
                break
        else:
            new_calendar = reminders.Calendar()
            new_calendar.title = CALENDAR
            new_calendar.save()
            self.calendar = new_calendar

    def add(self, title):
        r = reminders.Reminder(self.calendar)
        r.title = title
        r.save()
