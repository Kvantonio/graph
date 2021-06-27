"""
    There will be algorithms that may come in
    handy in the future

   Most algorithms will be written for practice
   and will not be of any use
"""

def gcd(number_one, number_two):
    """ recursive Euclid algorithm """
    if number_two == 0:
        return number_one
    return gcd(number_two, number_one % number_two)
