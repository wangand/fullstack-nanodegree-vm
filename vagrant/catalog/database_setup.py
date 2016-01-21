import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
import json


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    email = Column(String(255), nullable = False)
    name = Column(String(255), nullable = False)
    picture = Column(String)

    item = relationship("Item")

    def __repr__(self):
      return "<User(name='%s', email='%s', id='%s')>" % (
                                self.name, self.email, self.id)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key = True)
    category_name = Column(String(255), nullable = False)

    item = relationship("Item")

    def __repr__(self):
      return "<Category(name='%s', id='%s')>" % (
                                self.category_name, self.id)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key = True)
    item_name = Column(String(255), nullable = False)
    description = Column(String, nullable = False)
    cat_id = Column(Integer, ForeignKey('categories.id'), nullable = False)
    creator = Column(Integer, ForeignKey('users.id'), nullable = False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
      return "<Item(name='%s', id='%s', description='%s', category='%s', creator='%s')>" % (
                                self.item_name, self.id, self.description, self.cat_id, self.creator)


# Setup and bind sqlite3 engine
# session variable used by application.py
engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def return_one_category(name):
    """
    This function returns exactly 1 category id
    The id will match the name given
    Returns "Error" if not able to return exactly 1 category id
    """
    try: 
        cat_id = session.query(Category).filter(Category.category_name==name).one().id
        return cat_id
    except MultipleResultsFound:
        return "ERROR"
    except NoResultFound:
        return "ERROR"
    except:
        return "ERROR"


def return_one_user(email):
    """
    This function returns exactly 1 user id
    The id will match the email given
    Returns "Error" if not able to return exactly 1 user id
    """
    try:
        u_id = session.query(User).filter(User.email==email).one().id
        return u_id
    except MultipleResultsFound:
        return "ERROR"
    except NoResultFound:
        return "ERROR"
    except:
        return "ERROR"


# This function returns:
# number of categories
# list of (id, category_name) tuples
def get_categories():
    query = session.query(Category)
    size = query.count()
    cat_list = [(x.id, x.category_name) for x in query]
    return (size, cat_list)


# This function makes json thing
def make_json():
    items = session.query(Item)
    cats = session.query(Category)
    #size, cats = get_categories()
    the_list = [{'id':x.id, 'name':x.category_name, 'item':None} for x in cats]
    for i in the_list:
        filtered = items.filter(Item.category == i['id'])
        inner_list = []
        for k in filtered:
            inner_list.append({
                'id': k.id,
                'cat_id': k.category,
                'description': k.description,
                'name': k.item_name
                })
        i['item'] = inner_list
    printable = json.dumps({"Category": the_list})
    print printable
