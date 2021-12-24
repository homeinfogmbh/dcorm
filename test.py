"""Basic debugging."""

from datetime import datetime

from dcorm import field, select, Model
from dcorm.engine import Engine


class MyModel(Model):

    id: int
    name: str
    created: datetime = field(default_factory=datetime.now)


def main():

    engine = Engine()
    print('Engine:', engine, engine._sql)
    record = MyModel(3, 'Pee-Wee Herman')
    print('Record:', record)
    print('Field:', MyModel.id, type(MyModel.id))
    condition = (~(MyModel.id == 1)) & (MyModel.name == 'Monty')
    print('Condition:', condition)
    query = select(MyModel).where(condition)
    print('Engine:', engine := query.__sql__(engine))
    print('Query:', engine.query_string())


if __name__ == '__main__':
    main()
