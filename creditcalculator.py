""" C R E D I T    C A L C U L A T O R
Owner            : https://github.com/veena-LINE
Python version   : 3.8.1
Last Modified    :
File Created     : 2020 Jul 17
File History     : 2020 Jul 17 - File created
"""

from math import ceil, log
from sys import argv


class CreditCalculator:
    """ Utility to compute parameters of 'the Credit'.
    There are two kinds of credit:
    1. Annuity payment (fixed payment for the whole credit term)
    2. Differentiated payment (variable payment)

    :: Annuity payment ::
        Formula for calculating the Ordinary Annuity payment (A):
                          (i * pow(1 + i, n))
                A =   P * -------------------
                          (pow(i + i, n) - 1)
        where,
        A: Ordinary Annuity Payment
        P: Credit principal
        i: Nominal (monthly) interest rate.
           Usually this is 1/12th of the annual interest rate.
           It's a floating value, not a percentage.
           For example, if you have an annual interest rate of 12%, then i = 0.01
        n: Number of payments in months.

        A, P, i and n values are of interest.
        Each of these values can be calculated if others are known.
                                     A
                P = -------------------------------------
                    (i * pow(1+i, n)) / (pow(1+i, n) - 1)

                n = log( A/(A - i*P), 1+i)
                                       ^is the log base

    :: Differentiated payment ::
        Formula for calculate the Differentiated Payment D(m):
                        P                P * (m - 1)
                D(m) = ---  +  i * (P - -------------)
                        n                     n
        where,
        D(m): mth Differentiated Payment
        m: Current period
        P: Credit Principal
        i: Nominal monthly interest rate
        n: Number of payments in months
    """

    def __init__(self):
        self.__user_choice = ''
        self.__credit_principal = 0
        self.__credit_interest = 0.0
        self.__principal_term = 0
        self.__annuity_monthly = 0.0
        self.__calculation_type = ''
        self.__DIFFERENTIATED_PAY = 'diff'
        self.__ANNUITY = 'annuity'
        self.__SEEK_ANNUITY_MONTHLY = 'm'
        self.__SEEK_TERM = 't'
        self.__SEEK_CREDIT_PRINCIPAL = 'p'
        self.__differentiated_pay = []
        self.__overpayment = 0

    @staticmethod
    def usage():
        print('''
        Calculate Annuity/Differentiated Payment
        by passing necessary values:
        
        Usage: On a single line type,
            python creditcalculator.py --<parameter=> --<parameter=> so on

        Example 1:           Example 2:         Example 3:       Example 4:
        --type=diff          --type=annuity     --type=annuity   --type=annuity
        --principal=1000000  --principal=50000  --payment=8722   --principal=
        --term=10            --term=8           --term=120       --payment=
        --interest=10        --interest=7.8     --interest=5.6   --interest=

        ^                    ^                  ^                ^
        Calculates           Calculates         Calculates       Calculates
        Variable             Annuity            Credit           Credit
        Payments             Monthly            Principal        Term
        
        --term, in months. Convert years to months.
        --interest, type without the percentage. Can be a floating value.
        ''')

    def process_arguments(self, args):
        """ Process user arguments and determine further course of action.
        If the user desires 'diff' differentiated payment,
         calculate month-wise payments.
        If the user desires 'annuity', figure out if principal,
         term or the monthly annuity needs computation.
        :param args: Holds command-line user input.
        :return: None
        """
        diff_parameters = {'diff', 'p', 't', 'i'}
        annuity_parameters = {'annuity', 'p', 't', 'i', 'm'}
        params = set()

        for arg in args:
            if 'type' in arg:
                self.__calculation_type = arg.split('=')[1]
                params.add(self.__calculation_type)
            elif 'principal' in arg:
                self.__credit_principal = int(arg.split('=')[1])
                params.add('p' if 'p' not in params else '')
            elif 'term' in arg:
                self.__principal_term = int(arg.split('=')[1])
                params.add('t' if 't' not in params else '')
            elif 'interest' in arg:
                self.__credit_interest = float(arg.split('=')[1])\
                                       / (12 * 100)
                params.add('i' if 'i' not in params else '')
            elif 'payment' in arg:
                self.__annuity_monthly = float(arg.split('=')[1])
                params.add('m' if 'm' not in params else '')

        if self.__calculation_type == self.__DIFFERENTIATED_PAY and (diff_parameters - params):
            self.__calculation_type = ''
        elif self.__calculation_type == self.__ANNUITY:
            self.__user_choice = ''.join(annuity_parameters - params)

    def calculate(self):
        """ Differentiated monthly payments / Annuity information is self-explanatory.
        Finally, overpayment is calculated and displayed.
        :return: None
        """
        if self.__calculation_type == self.__DIFFERENTIATED_PAY:
            for month in range(1, self.__principal_term+1):
                self.__differentiated_pay.append(
                    ceil(
                        (self.__credit_principal/self.__principal_term)
                        + self.__credit_interest*(self.__credit_principal
                                                  - (self.__credit_principal
                                                     * (month-1))
                                                  / self.__principal_term)
                    )
                )
            self.__overpayment = sum(self.__differentiated_pay) - self.__credit_principal

            for i, dp in enumerate(self.__differentiated_pay, 1):
                print(f'Month {i}: paid out {dp}')
            print()
            print(f'Overpayment = {self.__overpayment}')

        elif self.__calculation_type == self.__ANNUITY:
            if self.__user_choice == self.__SEEK_ANNUITY_MONTHLY:
                self.__annuity_monthly = ceil(
                    self.__credit_principal * ((self.__credit_interest
                                                * pow(1+self.__credit_interest
                                                      , self.__principal_term)
                                                )
                                               / (pow(1+self.__credit_interest
                                                      , self.__principal_term)
                                                  - 1)
                                               )
                )
                self.__overpayment = (self.__annuity_monthly * self.__principal_term
                                      - self.__credit_principal
                                      )
                print(f'Your annuity payment = {self.__annuity_monthly}!')

            elif self.__user_choice == self.__SEEK_TERM:
                self.__principal_term = ceil(
                    log(self.__annuity_monthly / (self.__annuity_monthly
                                                  - (self.__credit_interest
                                                     * self.__credit_principal))
                        , 1+self.__credit_interest)
                )
                self.__overpayment = ceil(self.__annuity_monthly
                                          * self.__principal_term
                                          - self.__credit_principal
                                          )
                years = self.__principal_term // 12
                months = self.__principal_term % 12

                print(f'You need {years} year{"s" if self.__principal_term > 1 else ""}'
                      f'{" and " + str(months) + " months" if months > 0 else ""}'
                      f' to repay this credit!')

            elif self.__user_choice == self.__SEEK_CREDIT_PRINCIPAL:
                self.__credit_principal = ceil(
                    self.__annuity_monthly
                    / ((self.__credit_interest
                        * pow(1+self.__credit_interest, self.__principal_term)
                        )
                       / (pow(1+self.__credit_interest, self.__principal_term)
                          - 1)
                       )
                )
                self.__overpayment = ceil(self.__annuity_monthly
                                          * self.__principal_term
                                          - self.__credit_principal)

                print(f'Your credit principal = {self.__credit_principal}!')
            print(f'Overpayment = {self.__overpayment}')

        else:
            print('Incorrect parameters')
            self.usage()


if __name__ == '__main__':
    arguments = argv

    if len(arguments) < 5:
        print('Incorrect parameters')
        print()
        CreditCalculator.usage()
    else:
        credit_calc = CreditCalculator()
        credit_calc.process_arguments(arguments[1:])
        print()
        credit_calc.calculate()
