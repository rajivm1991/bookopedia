from sqlalchemy import sql, Column, Integer, DateTime, ForeignKey, Float, SmallInteger, Unicode
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql import ClauseElement
from sqlalchemy_utils import URLType

__all__ = ['session', 'get_or_create', 'Book', 'Category']


engine = create_engine('postgresql+psycopg2://bookopedia:bookopedia@bookopedia_postgres/bookopedia', echo=True)
session = sessionmaker(bind=engine)()
ModelBase = declarative_base()


class Book(ModelBase):
    __tablename__ = 'book'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', Unicode(255), nullable=False, index=True, unique=True)
    thumbnail = Column('thumbnail', URLType, nullable=True)
    rating = Column('rating', SmallInteger, nullable=True)
    price = Column('price', Float, nullable=False, default=0)
    currency = Column('currency', Unicode(1), nullable=False, index=True)
    availability = Column('availability', Unicode(15), nullable=False, index=True)
    category = Column('category', Integer, ForeignKey("category.id"), nullable=False, index=True)
    created_at = Column('created_at', DateTime(), nullable=False, server_default=sql.func.now())
    updated_at = Column('updated_at', DateTime(), nullable=False, server_default=sql.func.now(), onupdate=sql.func.now())

    # relations
    category_obj = relationship("Category", back_populates="book_set")  # type: Category

    def __repr__(self):
        return "<%s %d - %s>" % (self.__class__.__name__, self.id, self.title)


class Category(ModelBase):
    __tablename__ = 'category'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', Unicode(255), nullable=False)
    slug = Column('slug', Unicode(255), nullable=False, index=True, unique=True)

    # relations
    book_set = relationship("Book", back_populates="category_obj")


def get_or_create(session, model, defaults=None, **kwargs):
    print('KWARGS', kwargs)
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True
