import pandas as pd
import math
from data_loader import DataLoader

class RiskAnalyzer:
    """Analyze LVHM stock data to detect periods of market ris. 
    Uses DataLoader to access cleaned data"""

    def __init__(self, loader: DataLoader, volatility_window: int = 20, risk_threshold: float = 0.015):
        """Initialize the Analyzer"""
        self.df = loader.get_data().copy()
        self.volatility_window = volatility_window
        self.risk_threshold = risk_threshold
        self.results = None

    def compute_daily_returns(self):
        """compute daily returns for each trading day"""
        self.df["Daily_Return"] = self.df["Price"].pct_change()
        return self.df["Daily_Return"]
    
    def compute_volatility(self):
        """compute the rolling volatility as std of daily returns over the specified window of trading days"""
        if "Daily_Return" not in self.df.columns:
            self.compute_daily_returns()
        self.df["Volatility"] = self.df["Daily_Return"].rolling(window = self.volatility_window).std()
        return self.df["Volatility"]

    def compute_moving_average(self, window: int = 50):
        """compute the moving average of stock price"""
        col_name = f'MA_{window}'
        self.df[col_name] = self.df["Price"].rolling(window=window).mean()
        return self.df[col_name]
    
    def compute_max_drawdown(self):
        """comput the maximum drawdown over the dataset"""
        rolling_max = self.df["Price"].cummax()
        drawdown = (self.df["Price"] - rolling_max) / rolling_max
        return round(drawdown.min(),4)
    
    def label_risk_level(self):
        """Label each trading day as "elevated" or "normal" risk based on if volatility exceeds threshold"""
        if "Volatility" not in self.df.columns:
            self.compute_volatility()
        
        self.df["Risk_Level"] = self.df["Volatility"].apply(
            lambda v: "elevated" if (not math.isnan(v) and v> self.risk_threshold) else "normal")
        return self.df["Risk_Level"]
    
    def run_analysis(self):
        """run full ris analysis pipeline and return results"""
        self.compute_daily_returns()
        self.compute_volatility()
        self.compute_moving_average(window=50)
        self.compute_moving_average(window=200)
        self.label_risk_level()
        self.results = self.df
        return self.results
    
    def get_high_risk_days(self):
        """return a list of days lebeled as elevated risk"""
        if self.results is None:
            self.run_analysis()
        return [str(row["Date"].date()) for _, row in self.results.iterrows() if row["Risk_Level"] == "elevated"]
    
    def risk_signal_generator(self):
        """ generator yields risk signals one by one.yileds a message for each day indicating elevated"""
        if self.results is None:
            self.run_analysis()
        for _ , row in self.results.iterrows():
            if row["Risk_Level"] == "elevated":
                yield f"{row['Date'].date()} | Volatility: {row['Volatility']:.4f} | Elevated Risk Detected"

    def __str__(self):
        """return a summary of analysis"""
        return (f"RiskAnalyzer | Window: {self.volatility_window} days | Risk Threshold: {self.risk_threshold}\n")
    
    def __len__(self):
        """return number od trading days analyzed"""
        return len(self.df)
    
if __name__ == "__main__":
    from data_loader import DataLoader
    loader = DataLoader('Louis Vuitton Stock Price History.csv')
    analyzer = RiskAnalyzer(loader)

    results = analyzer.run_analysis()
    print(analyzer)
    print(f"\nMax Drawdown: {analyzer.compute_max_drawdown():.2%}")

    high_risk = analyzer.get_high_risk_days()
    print(f"\nHigh risk days: {len(high_risk)}")
    print(f"First 5 high risk days: {high_risk[:5]}")

    print("\nFirst 3 risk signals:")
    gen = analyzer.risk_signal_generator()
    for _ in range(3):
        print(next(gen))