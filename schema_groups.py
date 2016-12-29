"""Schema tables for Mambu Groups.

TODO: this are just very basic schemas for groups. A some fields
are missing.
"""

from mambupy import schema_orm as orm
from mambupy.schema_branches import Branch
from mambupy.schema_users import User
from mambupy.schema_addresses import Address

from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey
from sqlalchemy import Column, String, DateTime, Numeric, Integer

dbname = orm.dbname
session = orm.session
Base = orm.Base

class Group(Base):
    """Group table.
    """
    __tablename__  = "group"
    __table_args__ = {'schema'        : dbname,
                      'keep_existing' : True
                     }

    # Columns
    encodedkey = Column(String, primary_key=True)
    id         = Column(String, index=True, unique=True)
    groupname  = Column(String)
    loancycle  = Column(Integer)

    # Relationships
    assignedbranchkey = Column(String, ForeignKey(Branch.encodedkey))
    branch            = relationship(Branch, backref=backref('groups'))
    assigneduserkey   = Column(String, ForeignKey(User.encodedkey))
    user              = relationship(User, backref=backref('groups'))
    addresses         = relationship(Address,
                                     backref=backref('group'),
                                     foreign_keys=[Address.parentkey],
                                     primaryjoin='Address.parentkey == Group.encodedkey')

    def __repr__(self):
        return "<Group(id={}, groupname={})>".format(self.id, self.groupname)
