from scipy.optimize import fsolve, minimize
import numpy as np

def Profit(P, A, MC, Share):
    '''
    P: Price matrix
    A: Observable attributes matrix
    MC: Marginal cost matrix
    Share: Market share matrix
    '''
    return (P-MC)*Share(P, A)



def Monopoly_Prices(P0, A, MC, Share, tol=1e-10):
    return minimize(fun = lambda x: -np.sum(Profit(x, A, MC, Share)), 
                    x0 = P0,
                    tol=tol
                    ).x

def Set_Price(P, i, p):
    P[i] = p
    return P


def Best_Response(P, A, MC, Share, i):
    fun = lambda p: -Profit(Set_Price(P, i, p), A, MC, Share)[i]
    result = minimize(fun, 
                    P[i],
                    tol=1e-10
                    )
    return result.x[0]


def IBR(P0, A, MC, Share, maxit=1000, tol=1e-8):
    success = False
    P = np.array([Best_Response(P0, A, MC, Share, i) for i in range(len(P0))])
    for i in range(maxit):
        P_new = np.array([Best_Response(P, A, MC, Share, i) for i in range(len(P0))])
        if np.linalg.norm(P_new - P) < tol:
            print(f'IBR successful after {i} iterations')
            success = True
            break
        P = P_new

    if not success:
        print(f'IBR failed after {i} iterations')

    return P_new



def Newton(P0, A, MC, Share, tol=1e-10):
    fun = lambda p: np.array(p) - np.array([Best_Response(p, A, MC, Share, i) for i in range(len(P0))])

    return fsolve(fun, P0, xtol=tol)
    

def Make_Price_Ranges(Nash, Mono, num_p, include_NE_and_Mono=True, extra=0.1):

    more = extra * (Mono-Nash)

    start = Nash-more
    end = Mono+more

    price_ranges = []

    assert len(Nash) == len(Mono)
    
    for i in range(len(Nash)):
        if include_NE_and_Mono:
            pricerange = np.linspace(start[i], end[i], num_p-2)
            price_ranges.append(np.sort(np.concatenate(([Nash[i], Mono[i]], pricerange))))
        else:
            price_ranges.append(np.linspace(start[i], end[i], num_p))
            
    return price_ranges

def get_collusion_quotient(average: np.array, nash: np.array, monopoly:np.array):
    return (average- nash)/(monopoly-nash)


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def find_closest(value, action_space):
    """Finds the closest value in the given sorted action space."""
    return min(action_space, key=lambda x: abs(x - value))