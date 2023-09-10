from sympy import symbols, Eq, solve

class Definitions:
    def LCOE(self, capital_cost, operational_cost, capacity_factor, project_lifetime, discount_rate, n):
        total_costs = capital_cost + operational_cost * project_lifetime
        total_energy_production = capacity_factor * n * project_lifetime

        discount_factor = 1 / ((1 + discount_rate) ** project_lifetime)
        discounted_total_costs = total_costs * discount_factor

        lcoe = discounted_total_costs / total_energy_production
        return lcoe
    
    def FV(self, present_value, interest_rate, periods, fv):
        PV, IR, p, FV = symbols('PV IR p FV')
        # future_value = present_value * (1 + interest_rate)**periods
        equation = Eq(PV * ((1 + IR) ** p), FV)
        #equation = Eq(PV + 1 + IR + p, FV)
        one = [present_value, interest_rate, periods, fv]
        list_symbols = [PV, IR, p, FV]
        count = 0
        given_values = dict()
        for i in one:
            if i != None:
                given_values[str(list_symbols[count])] = one[count]
            count += 1 
        count = 0
        for i in one:
            if i == None:
                solution = solve(equation, list_symbols[count])
                if solution:
                    solution_value = solution[0].subs(given_values)
                    vars = ["Present Value", "Interest Rate", "Period", "Future Value"]
                    var = vars[count]
                    return solution_value, var
            count += 1
        return None
    
    def HR(self, cost_of_equity, cost_of_debt, tax_rate, equity_weight, debt_weight):
        wacc = (cost_of_equity * equity_weight) + ((cost_of_debt * (1 - tax_rate)) * debt_weight)
        return wacc
    
    def IRR(self, cash_flows):
        import numpy_financial as np
        irr = np.irr(cash_flows)
        return irr




Defs = Definitions()

'''
capital_cost = 10000000  # $10 million
operational_cost = 1000000  # $1 million per year
capacity_factor = 0.35  # 35% capacity factor
project_lifetime = 20  # 20 years
n = 8760  # 8760 hours in a year
discount_rate = 0.08  # 8%
lcoe = Defs.LCOE(capital_cost, operational_cost, capacity_factor, project_lifetime, discount_rate, n)
print((f"LCOE: ${lcoe:.2f} / MWh"))
'''


present_value = 1000  # Initial investment
interest_rate = 0.05  # 5% interest rate
periods = 10         # Number of periods (years)
fv = None            # Future value

future_value, var = Defs.FV(present_value, interest_rate, periods, fv)
print(f"{var}: ${future_value:.2f}")


'''
cost_of_equity = 0.10   # 10% cost of equity
cost_of_debt = 0.06     # 6% cost of debt
tax_rate = 0.3         # 30% tax rate
equity_weight = 0.6     # 60% equity weight
debt_weight = 0.4       # 40% debt weight

hurdle_rate = Defs.HR(cost_of_equity, cost_of_debt, tax_rate, equity_weight, debt_weight)
# Weighted Average Cost of Capital
print(f"Hurdle Rate (WACC): {hurdle_rate:.2%}")
'''

'''
cash_flows = [-1000, 300, 300, 300, 300]

irr = Defs.IRR(cash_flows)
print(f"IRR: {irr:.2%}")
'''
