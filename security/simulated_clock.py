from datetime import datetime


class SimulatedClock:

    def __init__(self, current_time="10:00"):
        self.current_time = current_time

    def get_time(self):
        return self.current_time

    def set_time(self, new_time):
        self.current_time = new_time

    def is_within(self, valid_from, valid_until):
        current = datetime.strptime(
            self.current_time,
            "%H:%M"
        )

        start = datetime.strptime(
            valid_from,
            "%H:%M"
        )

        end = datetime.strptime(
            valid_until,
            "%H:%M"
        )

        return start <= current <= end