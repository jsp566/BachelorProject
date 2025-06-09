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

def Specific_Profit(P, A, MC, Share, i):
    '''
    P: Price matrix
    A: Observable attributes matrix
    MC: Marginal cost matrix
    Share: Market share matrix
    i: products indexes
    '''
    this_prof = np.array(Profit(P, A, MC, Share))
    total = this_prof[i].sum()
    return total

def Set_Price(P, i, p):
    '''
    Set price for products in i to p
    P: Price matrix
    i: product indexes
    p: prices to set
    '''
    if type(i) == int:
        i = [i]
    if type(p) == float:
        p = [p]
    for j in i:
        P[j] = p[j]
    return P


def Best_Response(P0, A, MC, Share, i):
    fun = lambda p: -Specific_Profit(Set_Price(P0, i, p), A, MC, Share, i)
    result = minimize(fun, 
                    P0,
                    tol=1e-10
                    )
    
    return np.array(result.x)[i]

# owner_structure is list of lists
# [[0,1], [2,3]] means that firm 0 are producing products 0 and 1, and firm 1 is producing products 2 and 3
# [[0,1], [2]] means that firm 0 is producing products 0 and 1, and firm 1 is producing product 2


def market_reaction(p, A, MC, Share, owner_structure):
    '''
    p: Price matrix
    A: Observable attributes matrix
    MC: Marginal cost matrix
    Share: Market share matrix
    owner_structure: list of lists of indexes of products owned by each firm
    '''
    P = np.zeros(len(p))

    for i, products in enumerate(owner_structure):
        new_prices = Best_Response(p, A, MC, Share, products)
        for j, product in enumerate(products):
            P[product] = new_prices[j]
        
    return P

def Newton(P0, A, MC, Share, tol=1e-10, owner_structure=None):

    if owner_structure is None:
        owner_structure = [[x] for x in range(len(P0))]

    fun = lambda p: np.array(p) - np.array(market_reaction(p, A, MC, Share, owner_structure))

    return fsolve(fun, P0, xtol=tol)
  

def Monopoly_Prices(P, A, MC, Share):
    all_indexes = list(range(len(P)))
    
    return Newton(P, A, MC, Share, owner_structure=[all_indexes])

  

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
    return min(action_space, key=lambda x: sum(abs(x - value)))