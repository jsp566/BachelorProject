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



def Monopoly_Prices(P0, A, MC, Share):
    return minimize(fun = lambda x: -np.sum(Profit(x, A, MC, Share)), 
                    x0 = P0
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
    P = P0
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



def Newton(P0, A, MC, Share):
    fun = lambda p: np.array(p) - np.array([Best_Response(p, A, MC, Share, i) for i in range(len(P0))])

    return fsolve(fun, P0, xtol=1e-10)
    



def Make_Price_Range(P0, A, MC, Share, i, num_p, include_NE_and_Mono=True, extra=0.1):
    NE = Newton(P0, A, MC, Share)[i]
    Mono = Monopoly_Prices(P0, A, MC, Share)[i]

    if include_NE_and_Mono:
        start = NE*(1-extra)
        end = Mono*(1+extra)
        result = np.linspace(start, end, num_p-2)
        return np.sort(np.concatenate(([NE, Mono], result)))

    else:
        start = NE*(1-extra)
        end = Mono*(1+extra)
        return np.linspace(start, end, num_p)

def get_collusion_quotient(average: np.array ,nash: np.array, monopoly:np.array):
    return (average- nash)/(monopoly-nash)

