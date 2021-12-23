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
    query = select(MyModel).where(MyModel.id == 1)
    print('Query:', query.__sql__)


if __name__ == '__main__':
    main()
