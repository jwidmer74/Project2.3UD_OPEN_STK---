from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup2 import Category, Base, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

category1 = Category(name="Soccer")

session.add(category1)
session.commit()

Item2 = Item(name="net", description="AmazonBasics Soccer Goal",
                     price="$15.50",material="other", category=category1)

session.add(Item2)
session.commit()


Item1 = Item(name="backboard", description="JAPER BEES Mini PRO Over The Door & Wall Mount Basketball Hoop w/Thick Shatterproof Backboard ",
                     price="$50.50",material="plastic", category=category1)

session.add(Item1)
session.commit()



category2 = Category(name="Basketball")
session.add(category2)
session.commit()

Item2 = Item(name="basketball", description="Spalding NBA Indoor/Outdoor Replica Game Ball",
                     price="$6.50",material="other", category=category2)

session.add(Item2)
session.commit()


Item1 = Item(name="Googles", description="COPOZZ Ski Goggles, G1 OTG Snowboard Snow Goggles for Men Women Youth Anti-Fog UV Protection, Polarized Lens Available",
                     price="$10.50",material="plastic", category=category2)

session.add(Item1)
session.commit()

category3 = Category(name="Baseball")

session.add(category3)
session.commit()

Item2 = Item(name="bat", description="Cold Steel Brooklyn Smasher ",
                     price="$4.50",material="metal", category=category3)

session.add(Item2)
session.commit()


Item1 = Item(name="glove", description="Wilson A2000 SuperSkin Baseball Glove Series ",
                     price="$25.50",material="other", category=category3)

session.add(Item1)
session.commit()

category4 = Category(name="Frisbee")

session.add(category4)
session.commit()

Item2 = Item(name="Frisbee Net", description="Champion Sports Disc Target Net",
                     price="$8.50",material="metal", category=category4)

session.add(Item2)
session.commit()


Item1 = Item(name="Signed Frisbee", description="Casey Stengel PSA DNA Autograph Twice Signed Disc Authenticated ",
                     price="$15.50",material="plastic", category=category4)

session.add(Item1)
session.commit()

category5 = Category(name="Snowboarding")

session.add(category5)
session.commit()

Item2 = Item(name="Snow Board gooogles", description="Revo RG 7008 Wordsmith Polarized Ski Goggles ",
                     price="$5.50",material="plastic", category=category5)

session.add(Item2)
session.commit()


Item1 = Item(name="Snowboards", description="Ride Manic Snowboard Mens ",
                     price="$115.50",material="plastic", category=category5)

session.add(Item1)
session.commit()

print "added items!"
