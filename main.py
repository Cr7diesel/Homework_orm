import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = 'postgresql://postgres:python123@localhost:5432/my_db'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


publisher_id = int(input('Введите id издательства: '))

if 0 < publisher_id < 5:
    q = session.query(Publisher).filter(Publisher.id == publisher_id).all()
    for s in q:
        print(f'Книги издательства {s.name} продаются в магазинах: ')
    q1 = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.id == publisher_id).all()
    for shop in q1:
        print(shop.name)
else:
    print('Вы ввели неверный id')


session.close()
