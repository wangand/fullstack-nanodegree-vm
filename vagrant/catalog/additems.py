import database_setup
from database_setup import User, Category, Item, session, get_categories, make_json
from database_setup import return_one_category


"""
This script adds sample categories to database
"""


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
