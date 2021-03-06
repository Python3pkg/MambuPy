"""Schema tables for Mambu Loan Accounts.

TODO: this are just very basic schemas for loan tables. A lot of fields
are missing.
"""

from . import schema_orm as orm

from .schema_branches import Branch
from .schema_users import User

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Column, String, DateTime, Numeric, Integer

dbname = orm.dbname
session = orm.session
Base = orm.Base

class LoanProduct(Base):
    """LoanProduct table.
    """
    __tablename__  = "loanproduct"
    __table_args__ = {'schema'        : dbname,
                      'keep_existing' : True
                     }

    # Columns
    encodedkey     = Column(String, primary_key=True)
    id             = Column(String, index=True, unique=True)
    productname    = Column(String)
    activated      = Column(Integer)
    loans          = relationship('LoanAccount', back_populates='product')

    def __repr__(self):
        return "<LoanProduct(id=%s, name=%s)>" % (self.id, self.productname)


class DisbursementDetails(Base):
    """DisbursementDetails table.
    """
    __tablename__            = "disbursementdetails"
    __table_args__           = {'schema'        : dbname,
                                'keep_existing' : True
                               }

    # Columns
    encodedkey               = Column(String, primary_key=True)
    expecteddisbursementdate = Column(DateTime)
    disbursementdate         = Column(DateTime)
    firstrepaymentdate       = Column(DateTime)

    def __repr__(self):
        return "<DisbursementDetails(disbursementdate=%s)>" % (self.disbursementdate)


class LoanAccount(Base):
    """LoanAccount table.
    """
    __tablename__          = "loanaccount"
    __table_args__         = {'schema'        : dbname,
                              'keep_existing' : True
                             }

    # Columns
    encodedkey             = Column(String, primary_key=True)
    id                     = Column(String, index=True, unique=True)
    accountstate           = Column(String)
    accountsubstate        = Column(String)
    loanamount             = Column(Numeric(50,10))
    loanAmount             = Column(Numeric(50,10)) # redundant with same-as-RESTAPI-case
    notes                  = Column(String)
    principalbalance       = Column(Numeric(50,10))
    principalpaid          = Column(Numeric(50,10))
    principaldue           = Column(Numeric(50,10))
    interestbalance        = Column(Numeric(50,10))
    interestpaid           = Column(Numeric(50,10))
    interestdue            = Column(Numeric(50,10))
    interestrate           = Column(Numeric(50,10))
    interestcalculationmethod        = Column(String)
    interestbalancecalculationmethod = Column(String)
    repaymentinstallments  = Column(Integer)
    repaymentInstallments  = Column(Integer) # redundant with same-as-RESTAPI-case
    repaymentperiodunit    = Column(String)
    repaymentperiodcount   = Column(Integer)
    accountholdertype      = Column(String)
    feesbalance            = Column(Numeric(50,10))
    feespaid               = Column(Numeric(50,10))
    feesdue                = Column(Numeric(50,10))
    penaltybalance         = Column(Numeric(50,10))
    penaltypaid            = Column(Numeric(50,10))
    penaltydue             = Column(Numeric(50,10))
    creationdate           = Column(DateTime)
    approveddate           = Column(DateTime)
    closeddate             = Column(DateTime)

    # Relationships
    producttypekey         = Column(String, ForeignKey(LoanProduct.encodedkey))
    product                = relationship('LoanProduct', back_populates='loans')
    disbursementdetailskey = Column(String, ForeignKey(DisbursementDetails.encodedkey))
    disbursementdetails    = relationship('DisbursementDetails')
    assignedbranchkey      = Column(String, ForeignKey(Branch.encodedkey))
    branch                 = relationship('Branch', back_populates = 'loans')
    assigneduserkey        = Column(String, ForeignKey(User.encodedkey))
    user                   = relationship('User', back_populates = 'loans')
    accountholderkey       = Column(String)
    holder_group           = relationship('Group',
                                          back_populates = 'loans',
                                          foreign_keys   = 'LoanAccount.accountholderkey',
                                          primaryjoin    = 'LoanAccount.accountholderkey == Group.encodedkey')
    holder_client          = relationship('Client',
                                          back_populates = 'loans',
                                          foreign_keys   = 'LoanAccount.accountholderkey',
                                          primaryjoin    = 'LoanAccount.accountholderkey == Client.encodedkey')
    custominformation      = relationship('CustomFieldValue',
                                          back_populates = 'loan',
                                          foreign_keys   = 'CustomFieldValue.parentkey',
                                          primaryjoin    = 'CustomFieldValue.parentkey == LoanAccount.encodedkey')
    activities             = relationship('Activity', back_populates='loan')
    repayments             = relationship('Repayment', back_populates='account')
    transactions           = relationship('LoanTransaction', back_populates='account')

    def __repr__(self):
        return "<LoanAccount(id=%s, accountstate=%s)>" % (self.id, self.accountstate)


class Repayment(Base):
    """Repayment table.
    """
    __tablename__    = "repayment"
    __table_args__   = {'schema'        : dbname,
                        'keep_existing' : True
                       }

    # Columns
    encodedkey       = Column(String, primary_key=True)
    duedate          = Column(DateTime, index=True)
    state            = Column(String, index=True)
    principaldue     = Column(Numeric(50,10))
    principalpaid    = Column(Numeric(50,10))
    interestdue      = Column(Numeric(50,10))
    interestpaid     = Column(Numeric(50,10))
    feesdue          = Column(Numeric(50,10))
    feespaid         = Column(Numeric(50,10))
    penaltydue       = Column(Numeric(50,10))
    penaltypaid      = Column(Numeric(50,10))

    # Relationships
    parentaccountkey = Column(String, ForeignKey(LoanAccount.encodedkey))
    account          = relationship('LoanAccount',
                                    back_populates='repayments',
                                    order_by='Repayment.duedate')

    def __repr__(self):
        return "<Repayment(duedate=%s, state=%s,\naccount=%s)>" % (self.duedate.strftime('%Y%m%d'), self.state, self.account)


class LoanTransaction(Base):
    """LoanTransaction table.
    """
    __tablename__          = "loantransaction"
    __table_args__         = {'schema'        : dbname,
                              'keep_existing' : True
                             }

    # Columns
    encodedkey             = Column(String, primary_key=True)
    transactionid          = Column(Integer, index=True)
    amount                 = Column(Numeric(50,10))
    creationdate           = Column(DateTime)
    entrydate              = Column(DateTime)
    type                   = Column(String)
    principalamount        = Column(Numeric(50,10))
    interestamount         = Column(Numeric(50,10))
    feesamount             = Column(Numeric(50,10))
    penaltyamount          = Column(Numeric(50,10))
    reversaltransactionkey = Column(String)
    comment                = Column(String)

    # Relationships
    parentaccountkey       = Column(String, ForeignKey(LoanAccount.encodedkey))
    account                = relationship('LoanAccount',
                                          back_populates='transactions',
                                          order_by='LoanTransaction.transactionid')

    def __repr__(self):
        return "<LoanTransaction(transactionid=%s, amount=%s, creationdate=%s, entrydate=%s, type=%s, comment='%s', reversed=%s\naccount=%s)>" % (self.transactionid, self.amount, self.creationdate.strftime('%Y%m%d'), self.entrydate.strftime('%Y%m%d'), self.type, self.comment, "Yes" if self.reversaltransactionkey else "No", self.account)
