import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
import json
import sqlite3


"""
Drop tables to refresh schema
"""
conn = sqlite3.connect('catalog.db')
c = conn.cursor()
c.execute('drop table if exists items')
c.execute('drop table if exists users')
c.execute('drop table if exists categories')
conn.commit()
conn.close()
"""
End schema refresh
"""


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
engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Reset the Database
session.query(User).delete()
session.query(Category).delete()
session.query(Item).delete()


# Art Supplies Store Categories
cat_brush = Category(category_name = "Brushes")
cat_mats = Category(category_name = "Materials")
cat_pen = Category(category_name = "Pens")
session.add_all([
    cat_brush,
    cat_mats,
    cat_pen])


# Add users
user_me = User(email = "sekretemail@gmail.com", name = "Andrew")
session.add(user_me)


# commit to get access to ids
session.commit()


# Add 2 brushes and a pen from me

# get id corresponding to email
my_id = session.query(User).filter(User.email=="sekretemail@gmail.com").one().id


# This function makes sure we get one result
def return_one_category(name):
    try: 
        cat_id = session.query(Category).filter(Category.category_name==name).one().id
        return cat_id
    except MultipleResultsFound:
        print "More than one category found"
    except NoResultFound:
        print "No categories found"
    except:
        print "unkown error"

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


# get category ids
brush_id = return_one_category("Brushes")
#brush_id = session.query(Category).filter(Category.category_name=="Brushes").one().id
pen_id = return_one_category("Pens")

itm_paintbrush = Item(item_name = "paintbrush", description = "for paint", cat_id = brush_id, creator=my_id)
itm_dippen = Item(item_name = "dippen", description = "for oil", cat_id = pen_id, creator=my_id)
itm_oilbrush = Item(item_name = "oilbrush", description = "for oil", cat_id = brush_id, creator=my_id)

session.add_all([
    itm_paintbrush,
    itm_dippen,
    itm_oilbrush])
session.commit()


#res = session.query(Categories)
#print json.dumps(res)
