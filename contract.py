"""
CSC148, Winter 2023
Project
"""
import datetime
from math import ceil
from typing import Optional
from bill import Bill
from call import Call

# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This class is not to be changed or instantiated. It is an Abstract Class.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>.
        This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class TermContract(Contract):
    """
    TermContract
    """

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        """
        """
        Contract.__init__(self, start)
        self.end_date = end
        self.money = TERM_DEPOSIT

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """
        """
        billing = bill
        date = (month, year)
        month = self.start.month
        dollar = self.money
        years = self.start.year
        term_min = TERM_MINS
        self.curr_time = date
        fee = TERM_MONTHLY_FEE

        self.bill = billing
        a = "TERM"
        b = TERM_MINS_COST
        self.bill.set_rates(a, b)

        if not (self.curr_time != (month, years)):
            self.bill.add_fixed_cost(dollar)
        elif self.curr_time != (month, years):
            pass
        c = 0
        self.bill.free_min = c
        self.free_minutes = term_min
        self.bill.add_fixed_cost(fee)

    def bill_call(self, call: Call) -> None:
        """
        """
        free_min = self.free_minutes
        dur_call = ceil(call.duration / 60.0)
        amount = dur_call
        if free_min > amount:
            free_min -= amount
            self.bill.add_free_minutes(amount)
        elif not (free_min > amount):
            amount -= free_min
            self.bill.add_billed_minutes(amount)

    def cancel_contract(self) -> float:
        """
        """
        end_month = self.end_date.month
        time = self.curr_time
        dollar = -self.money
        end_year = self.end_date.year
        if time > (end_month, end_year):
            self.bill.add_fixed_cost(dollar)

        elif not (time > (end_month, end_year)):
            pass
        cost = self.bill.get_cost()
        return cost


class MTMContract(Contract):
    """Month to Month contract (child of Contract)
    """

    def __init__(self, start: datetime.date) -> None:
        """
        init
        """
        Contract.__init__(self, start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """
        """
        month_fee = MTM_MONTHLY_FEE
        billing = bill
        string = "MTM"
        self.bill = billing
        cost_min = MTM_MINS_COST
        billing.set_rates(string, cost_min)
        billing.add_fixed_cost(month_fee)


class PrepaidContract(Contract):
    """Prepaid contarct (child of Contract)

    === PUBLIC ATTRIBUTES ===
    balance:
        contract balance
    """
    balance: float

    def __init__(self, start: datetime.date, balance: int) -> None:
        """
        """
        Contract.__init__(self, start)

        self.fee = -balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """
        """
        billing = bill
        int1 = -10
        int2 = -25
        cost_min = PREPAID_MINS_COST
        string = "PREPAID"
        if self.fee > int1:
            self.fee += int2
        elif self.fee < int1:
            pass

        self.bill = billing
        self.bill.add_fixed_cost(self.fee)
        self.bill.set_rates(string, cost_min)

    def bill_call(self, call: Call) -> None:
        """
        """
        price = self.bill.get_cost()
        calc = ceil(call.duration / 60.0)

        self.fee = price
        self.bill.add_billed_minutes(calc)

    def cancel_contract(self) -> float:
        """
        """

        int0 = 0
        cost = self.fee
        if not (cost < 0):
            return cost
        elif cost < int0:
            return int0


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
