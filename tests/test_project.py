import pytest
import pandas as pd
from data_loader import DataLoader
from risk_analyzer import RiskAnalyzer

@pytest.fixture

def loader():
    """Load csv data for testing"""
    return DataLoader("Louis Vuitton Stock Price History.csv")

@pytest.fixture
def analyzer(loader):
    """Creates a RiskAnalyzer for testing"""
    return RiskAnalyzer(loader)

def test_loader_row_count(loader):
    """Test the dataset load the correct number of rows"""
    assert len(loader) == 2561

def test_loader_columns_exist(loader):
    """Test the required colums after cleaning"""
    df = loader.get_data()
    for col in ["Date","Price","Vol.","Change"]:
        assert col in df.columns

def test_loader_date_sorted(loader):
    """Test the dates are sorted in ascending order"""
    df = loader.get_data()
    assert df["Date"].is_monotonic_increasing

def test_loader_no_missing_price(loader):
    """Test if any missing values in price column"""
    df = loader.get_data()
    assert df["Price"].isnull().sum() == 0

def test_loader_str(loader):
    """Test the __str__ returns expected output"""
    result = str(loader)
    assert isinstance(result,str)
    assert len(result) > 0

def test_daily_return_length(analyzer):
    """Test the daily return series has correct length"""
    returns = analyzer.compute_daily_returns()
    assert len(returns) == 2561

def test_daily_return_first_is_nan(analyzer):
    """Test the first daily return is Nan because no previous day to compare"""
    returns = analyzer.compute_daily_returns()
    assert pd.isna(returns.iloc[0])

def test_volatility_length(analyzer):
    """Test the volatility series has correct length"""
    vol = analyzer.compute_volatility()
    assert len(vol) == 2561

def test_max_drawdown_nagative(analyzer):
    """Test the max drawdown is always either zero or negative"""
    drawdown = analyzer.compute_max_drawdown()
    assert drawdown <= 0

def test_risk_labels_valid(analyzer):
    """Test the risk labels are correctly assigned"""
    analyzer.run_analysis()
    valid_labels = {"elevated","normal"}
    assert set(analyzer.results["Risk_Level"].unique()).issubset(valid_labels)

def test_high_risk_days_is_list(analyzer):
    """Test high risk days returns a list"""
    days = analyzer.get_high_risk_days()
    assert isinstance(days, list)

def test_analyzer_str(analyzer):
    """Test the __str__ returns a string contains window infor"""
    result = str(analyzer)
    assert "20" in result

def test_summary_contains_high_risk_ratio(analyzer):
    """Test summary includes the high risk ratio and percent."""
    summary = analyzer.get_summary()
    assert "high_risk_ratio" in summary
    assert "high_risk_percent" in summary
    assert 0 <= summary["high_risk_ratio"] <= 1


def test_loader_invalid_file():
    """Test DataLoader raises an error for a missing file."""
    with pytest.raises(FileNotFoundError):
        DataLoader("missing_file.csv")


def test_invalid_volatility_window(loader):
    """Test RiskAnalyzer raises an error for invalid volatility window."""
    with pytest.raises(ValueError):
        RiskAnalyzer(loader, volatility_window=0)


def test_invalid_risk_threshold(loader):
    """Test RiskAnalyzer raises an error for invalid risk threshold."""
    with pytest.raises(ValueError):
        RiskAnalyzer(loader, risk_threshold=0)
