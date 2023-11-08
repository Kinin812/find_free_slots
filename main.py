from datetime import datetime, timedelta
from pprint import pprint


def convert_date(x: str) -> datetime:
    """Convert from string to datetime."""
    return datetime.strptime(x, "%H:%M")


def add_free_slot(start: datetime) -> dict:
    """Add new free slot."""
    return {'start': start, 'stop': (start + timedelta(minutes=30))}


class FreeSlots:
    """Class FreeSlots"""

    def __init__(self, busy_slots: list, start: str, stop: str, slot: int):
        self.busy = busy_slots
        self.start_work_day = convert_date(start)
        self.stop_work_day = convert_date(stop)
        self.slot_length = slot

        self.schedule: list[dict[datetime.time, datetime.time]] = [
            {'start': self.start_work_day, 'stop': self.start_work_day},
            {'start': self.stop_work_day, 'stop': self.stop_work_day}
        ]

        for i in range(len(self.busy)):
            self.schedule.append(
                {'start': datetime.strptime(self.busy[i]['start'],
                                            "%H:%M"),
                 'stop': datetime.strptime(self.busy[i]['stop'],
                                           "%H:%M")})
        self.schedule: list[dict[datetime.time, datetime.time]] = sorted(
            self.schedule, key=lambda x: x['start'])

    def find_free_slots(self) -> list[dict[str, str]]:
        """Find & add free slots."""
        result: list = []
        for i in range(len(self.schedule) - 1):
            end: datetime = self.schedule[i + 1]['start']
            start: datetime = self.schedule[i]['stop']
            free_slots_quantity: int = int(
                (end - start).seconds / 60 // self.slot_length)
            if free_slots_quantity > 0:
                new_start: datetime = start
                for _ in range(free_slots_quantity):
                    result.append(
                        {'start': new_start.strftime("%H:%M"),
                         'stop': (new_start + timedelta(
                             minutes=self.slot_length)).strftime("%H:%M")})
                    new_start: datetime = add_free_slot(new_start)['stop']

        return result


if __name__ == '__main__':
    # working day frames
    start_work_day, stop_work_day = '09:00', '21:00'
    # slot length
    slot_length = 30

    # busy time array
    busy = [
        {'start': '10:30', 'stop': '10:50'},
        {'start': '18:40', 'stop': '18:50'},
        {'start': '14:40', 'stop': '15:50'},
        {'start': '16:40', 'stop': '17:20'},
        {'start': '20:05', 'stop': '20:20'}
    ]
    res = FreeSlots(busy, start_work_day, stop_work_day, slot_length)
    pprint(res.find_free_slots())
