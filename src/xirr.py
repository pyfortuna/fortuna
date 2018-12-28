# https://codereview.stackexchange.com/questions/179099/user-defined-xirr-function-exception-handling

import datetime
from scipy import optimize

def xnpv(rate, cashflows):
    t0 = min(cashflows, key = lambda t: t[0])[0]
    return sum([cf/(1+rate)**((t-t0).days/365.0) for (t,cf) in cashflows])

def xirr(cashflows,guess=0.1):
    try:
        outc = optimize.newton(lambda r: xnpv(r, cashflows), guess, maxiter=100)
        if outc.imag == 0:
            return outc
        else:
            raise
    except (RuntimeError, OverflowError):
        try:
            outc = optimize.newton(lambda r: xnpv(r, cashflows), -guess, maxiter=100)
            if outc.imag == 0:
                return outc
            else:
                raise
        except (RuntimeError, OverflowError):
            return float("NaN")

#cftest = [(datetime.date(2001, 12, 5), -2000), (datetime.date(2007, 12, 5), -10), (datetime.date(2017, 12, 5), 20)]
cftest = [(datetime.date(2017, 9, 25), -10001), (datetime.date(2018, 12, 27), 11140)]
#cftest = [(datetime.date(2001, 12, 5), -2000), (datetime.date(2007, 12, 5), -1000), (datetime.date(2017, 12, 5), 20)]
print(cftest)
print(xirr(cftest))
