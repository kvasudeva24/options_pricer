import volatility as vol
import scipy
from volatility import historical_log_volatility
from volatility import parkinsons_volatility
from volatility import garman_klass_volatility
from volatility import rogers_satchell_volatility
from volatility import yang_zhang_volatility
from scipy.stats import Norm as N


def call_option(ticker, period_vol, period_opt):
    """
    Calculate the BSM price of a stock in a given period (time remaining and time for volatility).
    

    Parameters: 
    ticker: Stock ticker
    period_vol: Period in trading days to calculate volatility
    period: time remaining on the optoop

    Returns: BSM call-option price as a float
    """
