from Record import Record
from datetime import datetime
import json


def class_to_dict(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj.__dict__


class Note:
    def __init__(self) -> None:
        self.count = 0
        self.records = {}
        self.load_from_file()

    def add(self, title, text, created=datetime.now(), edited=datetime.now(),
            is_active=True):
        self.count = self.count + 1
        self.records[self.count] = Record(self.count, title, text,
                                          created,
                                          edited,
                                          is_active)
        self.save_to_file()

    def update_by_id(self, id, title, text, created, edited=datetime.now(),
                     is_active=True):
        rec = self.get_by_id(id)
        rec.update(title, text, created, edited, is_active)
        # rec.update(title, text, datetime.strptime(created, "%d.%m.%Y"),
        #            datetime.strptime(edited, "%d.%m.%Y"), is_active)
        self.records[id] = rec
        self.save_to_file()

    def get_by_id(self, id):
        return self.records.get(id)

    def del_by_id(self, id):
        rec = self.get_by_id(id)
        rec.deactivate()
        self.records[id] = rec
        self.save_to_file()

    def resurrect_by_id(self, id):
        rec = self.get_by_id(id)
        rec.activate()
        self.records[id] = rec
        self.save_to_file()

    def show_active(self):
        for id in self.records:
            rec = self.get_by_id(id)
            if rec.is_active:
                print(rec)

    def show_all(self):
        for id in self.records:
            print(self.get_by_id(id))

    def show_after_date(self, date):
        date = datetime.strptime(date, "%d.%m.%Y")
        for id in self.records:
            rec = self.get_by_id(id)
            if rec.created > date:
                print(rec)

    def show_by_date(self, date):
        date = datetime.strptime(date, "%d.%m.%Y")
        for id in self.records:
            rec = self.get_by_id(id)
            diff = rec.created - date
            if 0 <= diff.days < 1 and rec.is_active is True:
                print(rec)

    def save_to_file(self, file="data.json"):
        with open(file, "w") as wf:
            json.dump(self.records, wf, indent=4, default=class_to_dict)

    def load_from_file(self, file="data.json"):
        with open(file, "r") as rf:
            data = json.load(rf)
            for key in data:
                self.add(data.get(key)['title'],
                         data.get(key)['text'],
                         datetime.fromisoformat(data.get(key)['created']),
                         datetime.fromisoformat(data.get(key)['edited']),
                         data.get(key)['is_active'])
