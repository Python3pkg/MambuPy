# coding: utf-8
"""Mambu loan Repayments objects.

MambuRepayment holds a loan repayment. Don't instantiate this class
directly. Look at MambuRepayment pydoc for further info.

MambuRepayments holds a list of loan repayments.

Uses mambuutil.getrepaymentsurl as default urlfunc

Example response from Mambu for repayments (please omit comment lines beginning with #):
{
# Propiedades
"state": "PAID",

# Saldos
"principalDue": "200",
"interestDue": "1.5",
"principalPaid": "200",
"interestPaid": "1.5",

# Fechas
"dueDate": "2012-06-17T00:00:00+0000",
"lastPaidDate": "2012-06-12T00:00:00+0000",
"repaidDate": "2012-06-12T00:00:00+0000",

# Relaciones
"parentAccountKey": "8af63f2837e19ef50137e1d755510016",
"assignedUserKey": "8a5c1e9f34bdd2b90134c49b6b950948",
"assignedBranchKey": "8a70db342e6d595a012e6e7158670f9d"
"encodedKey": "8af63f2837e19ef50137e1d75563001c",
}

TODO: update this with later responses from Mambu, and perhaps certain
behaviours are obsolete here
"""


from .mambustruct import MambuStruct, MambuStructIterator
from .mambuutil import getrepaymentsurl


mod_urlfunc = getrepaymentsurl

class MambuRepayment(MambuStruct):
    """A loan Repayment from Mambu.

    Don't instantiate this class directly. It's mostly used by
    MambuRepayments to configure each of its elements as MambuRepayment
    objects. There's no suitable urlfunc to use to retrieve just a
    specific repayment from a loan account. In fact, you can look at the
    code of MambuRepayments.convertDict2Attrs(), it uses urlfunc and
    entid = None , so no connection to Mambu will be made, never, for
    any particular MambuRepayment object.
    """
    def __init__(self, urlfunc=mod_urlfunc, entid='', *args, **kwargs):
        """Tasks done here:

        Just initializes the MambuStruct.
        """
        MambuStruct.__init__(self, urlfunc, entid, *args, **kwargs)


    def __repr__(self):
        """Instead of the default id given by the parent class, shows
        the duedate of the repayment.
        """
        return self.__class__.__name__ + " - duedate: %s" % self['dueDate'].strftime("%Y-%m-%d")


class MambuRepayments(MambuStruct):
    """A list of loan Repayments from Mambu.

    You SHOULD give an entid at instantiation time: the id for the loan
    account which repayments you wish to retrieve.

    Makes no sense to send an empty entid, which throws a
    MambuError.
    """
    def __init__(self, urlfunc=mod_urlfunc, entid='', *args, **kwargs):
        MambuStruct.__init__(self, urlfunc, entid, *args, **kwargs)


    def __iter__(self):
        return MambuStructIterator(self.attrs)


    def convertDict2Attrs(self, *args, **kwargs):
        """The trick for iterable Mambu Objects comes here:

        You iterate over each element of the responded List from Mambu,
        and create a Mambu Repayment object for each one, initializing
        them one at a time, and changing the attrs attribute (which just
        holds a list of plain dictionaries) with a MambuRepayment just
        created.

        You send a None urlfunc and entid to each MambuRepayment,
        because there's no method to retrieve individual repayments from
        Mambu, nor each individual repayment is identified by a
        particular ID.
        """
        for n,r in enumerate(self.attrs):
            # ok ok, I'm modifying elements of a list while iterating it. BAD PRACTICE!
            try:
                params = self.params
            except AttributeError as aerr:
                params = {}
            kwargs.update(params)
            repayment = MambuRepayment(urlfunc=None, entid=None, *args, **kwargs)
            repayment.init(r, *args, **kwargs)
            self.attrs[n] = repayment
