import sqlalchemy
from sqlalchemy import create_engine
#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///:memory:')

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
    	return "<User(name='%s', fullname='%s', password='%s')>" % (
                                self.name, self.fullname, self.password)

Base.metadata.create_all(engine)
Base.metadata.bind = engine

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
#Session.configure(bind=engine)
session = Session()


ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)
session.commit()

ed_user.password = 'f8s7ccs'

session.add_all([
	User(name='wendy', fullname='Wendy Williams', password='foobar'),
	User(name='ed', fullname='Ed Smith', password='smith'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])


#
#for row in session.query(User, User.name).all(): 
#    print row.User, row.name

#query = session.query(User).filter(User.name == 'ed')
query = session.query(User).filter(User.name == 'mary')

from sqlalchemy.orm.exc import MultipleResultsFound
try: 
    user = query.one()
    print user
except MultipleResultsFound, e:
    print e


from sqlalchemy.orm.exc import NoResultFound
try: 
    user = query.filter(User.id == 99).one()
    print user
except NoResultFound, e:
    print e

# Counting
from sqlalchemy import func
query = session.query(User)
print query.count()
print session.query(func.count(User.name), User.name).group_by(User.name).all() 


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref=backref('addresses', order_by=id))
    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address
