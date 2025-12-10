#Create a class that calculates and stores financial metrics like beta, cost of debt, cost of equity, WACC, and ROIC.
import math
def safe(x):
    return 0 if (x is None or isinstance(x, float) and math.isnan(x)) else x
class FinancialMetrics:
    def __init__(self, ticker_df, spy_df, risk_free_rate, all_financials):
        self.ticker_df = ticker_df
        self.spy_df = spy_df
        self.risk_free_rate = risk_free_rate
        self.all_financials = all_financials
    # Calculate Beta
    def calculate_beta(self):
        ticker_returns = self.ticker_df['Close'].pct_change().dropna()
        spy_returns = self.spy_df['Close'].pct_change().dropna()
        covariance = ticker_returns.cov(spy_returns)
        variance = spy_returns.var()
        self.beta = covariance / variance
        return self.beta
    # Calculate Cost of Debt
    def calculate_cost_of_debt(self):
        if 'Interest Expense' in self.all_financials.columns:
            interest_expense = self.all_financials['Interest Expense'].iloc[-1]
        else:
            interest_expense = 0
        total_debt_end = self.all_financials['Total Debt'].iloc[-1]
        total_debt_start = self.all_financials['Total Debt'].iloc[-2]
        avg_debt = (total_debt_end + total_debt_start) / 2
        if avg_debt == 0:
            self.cost_of_debt = 0
        else:
            self.cost_of_debt = interest_expense / avg_debt
        return self.cost_of_debt
    
    # Calculate Cost of Equity using CAPM
    def calculate_cost_of_equity(self):
        beta = self.calculate_beta()
        self.cost_of_equity = self.risk_free_rate + beta * (0.06)  # Assuming market risk premium of 6%
        return self.cost_of_equity
    
    def calculate_tax_rate(self):
        pretax_income = self.all_financials['Pretax Income'].iloc[-1]
        tax_provision = self.all_financials['Tax Provision'].iloc[-1]
        if pretax_income == 0:
            self.tax_rate = 0
        else:
            self.tax_rate = tax_provision / pretax_income
        return self.tax_rate
    # Calculate WACC
    def calculate_wacc(self):
        tax_rate = self.calculate_tax_rate()
        cost_of_debt = self.calculate_cost_of_debt()
        cost_of_equity = self.calculate_cost_of_equity()
        debt = self.all_financials['Total Debt'].iloc[-1]
        equity = self.all_financials['Stockholders Equity'].iloc[-1]
        total_capital = debt + equity
        
        if total_capital == 0:
            self.wacc = 0.07
        else:
            weight_debt = debt / total_capital
            weight_equity = equity / total_capital
            after_tax_cost_of_debt = cost_of_debt * (1 - tax_rate)
            self.raw_wacc = (weight_debt * after_tax_cost_of_debt) + (weight_equity * cost_of_equity)
            self.wacc = max(self.raw_wacc, 0.07)
        if math.isnan(self.raw_wacc):
            print("WACC calculation failed. Please enter a manual WACC value:")
            manual = float(input("Manual WACC: "))
            self.wacc = manual
        return self.wacc
    # Compute all metrics
    def compute_all_metrics(self):
        self.calculate_beta()
        self.calculate_cost_of_debt()
        self.calculate_cost_of_equity()
        self.calculate_tax_rate()
        self.calculate_wacc()

