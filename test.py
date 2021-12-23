"""Basic debugging."""

from datetime import datetime

from dcorm import field, select, Model


class MyModel(Model):

    id: int
    name: str
    created: datetime = field(default_factory=datetime.now)


def main():

    record = MyModel(3, 'Pee-Wee Herman')
    print('Record:', record)
    print('Field:', MyModel.id, type(MyModel.id))
    condition = MyModel.id == 1
    print('Condition:', condition)
    query = select(MyModel).where(condition)
    print('Query:', query.__sql__)


if __name__ == '__main__':
    main()
