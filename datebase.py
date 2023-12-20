from peewee import *
import json
from datetime import date

db = SqliteDatabase('database.db')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def __call__(cls, *args, **kwargs):
        return cls.create(*args, **kwargs)

    @classmethod
    def get_all(cls):
        return [i for i in cls.select()]

    @classmethod
    def get_all_json(cls):
        fields = [field for field in cls._meta.fields.values() if
                  isinstance(field, (CharField, DateField))]  # Include appropriate field types
        data = []
        for instance in cls.select():
            item = {}
            for field in fields:
                value = getattr(instance, field.name)
                if isinstance(value, date):
                    value = value.strftime('%Y-%m-%d')  # Convert date to string in desired format
                item[field.name] = value
            data.append(item)

        return data

    @classmethod
    def get_json(cls, obj):
        fields = [field for field in cls._meta.fields.values() if
                  isinstance(field, (CharField, DateField))]
        data = []

        for instance in obj:
            item = {}
            for field in fields:
                value = getattr(instance, field.name)
                if isinstance(value, date):
                    value = value.strftime('%Y-%m-%d')
                item[field.name] = value
            data.append(item)
        return data

    @classmethod
    def get_by_id(cls, id):
        return cls.get(cls.id == id)

    @classmethod
    def get_by_name(cls, name):
        try:
            data = cls.select().where(cls.name.contains(name))
            return cls.get_json(data)
        except cls.DoesNotExist:
            return []

    @classmethod
    def get_by_original_pack(cls, original_pack):
        try:
            data = cls.select().where(cls.original_pack.contains(original_pack))
            return cls.get_json(data)
        except cls.DoesNotExist:
            return []

    @classmethod
    def get_by_base_price(cls, base_price):
        try:
            data = cls.select().where(cls.base_price.contains(base_price))
            return cls.get_json(data)
        except cls.DoesNotExist:
            return []

    @classmethod
    def get_by_expiration_date(cls, expiration_date):
        try:
            data = cls.select().where(cls.expiration_date.contains(expiration_date))
            return cls.get_json(data)
        except cls.DoesNotExist:
            return []

    @classmethod
    def get_by_manufacturer(cls, manufacturer):
        try:
            data = cls.select().where(cls.manufacturer.contains(manufacturer))
            return cls.get_json(data)
        except cls.DoesNotExist:
            return []

    @classmethod
    def get_by(cls, **kwargs):
        return cls.get(**kwargs)

    @classmethod
    def get_all_by(cls, **kwargs):
        return [i for i in cls.select().where(**kwargs)]

    @classmethod
    def filter(cls, obj_value):
        """
        Filter by name or id or original_pack or base_price or expiration_date or manufacturer
        :return: list of json data
        """
        data = cls.select().where(
            cls.name.contains(obj_value) |
            cls.original_pack.contains(obj_value) |
            cls.base_price.contains(obj_value) |
            cls.expiration_date.contains(obj_value) |
            cls.manufacturer.contains(obj_value)
        )
        fields = [field for field in cls._meta.fields.values() if
                  isinstance(field, (CharField, DateField))]  # Include appropriate field types
        json_data = []
        for instance in data:
            item = {}
            for field in fields:
                value = getattr(instance, field.name)
                if isinstance(value, date):
                    value = value.strftime('%Y-%m-%d')  # Convert date to string in desired format
                item[field.name] = value
            json_data.append(item)

        return json_data


class Drug(BaseModel):
    name = CharField()
    original_pack = CharField()
    base_price = CharField()
    expiration_date = DateField()
    manufacturer = CharField()

    class Meta:
        db_table = 'drug'

    def __str__(self):
        return self.name


def create_tables():
    db.create_tables([Drug])
    db.close()


def add_drug(name, original_pack, base_price, expiration_date, manufacturer):
    return Drug.__call__(name=name, original_pack=original_pack, base_price=base_price, expiration_date=expiration_date,
                         manufacturer=manufacturer)


def create_data():
    with open('data.json', 'r') as f:
        data = json.loads(f.read())

    for i in data:
        add_drug(
            name=i['name'],
            original_pack=i['original_pack'],
            base_price=i['base_price'],
            expiration_date=i['expiration_date'],
            manufacturer=i['manufacturer']
        )


if __name__ == '__main__':
    create_tables()
    create_data()
    print(Drug.get_all())
