def grad(pole):
    if ( pole[0] > pole[-1]):
        return 'RISING'
    else:
        return'FALLING'