# LVMH Stock Risk Monitoring System

## Team Members
| Name | Email | Stevens ID |
|------|-------|------------|
| Yihao He | yhe53@stevens.edu | 20038566 |
| Zhihao Wu | zwu50@stevens.edu | 20043443 |

---

## Project Description

### Overview
This project implements a rule-based risk monitoring system for LVMH stock prices from 2016 to 2026. 
Instead of predicting prices, the system identifies periods of elevated market risk using interpretable financial indicators 
including daily returns, rolling volatility, moving averages, and maximum drawdown.

### Dependencies
| Library | Purpose |
|------|------|
| pandas | Data loading, cleaning, and time-series processing |
| matplotlib | Visualization of price trends and volatility |
| pytest | Unit testing |
| math | Mathematical operations |

### File Structure
```
final/
├── data_loader.py        # DataLoader class: loads and cleans CSV data
├── risk_analyzer.py      # RiskAnalyzer class: computes indicators and risk labels
├── main.ipynb            # Main notebook: runs analysis and generates visualizations
├── tests/
│   └── test_project.py   # Pytest test cases
├── Louis Vuitton Stock Price History.csv
└── README.md
```

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/ChenLing0066/lv-risk-monitor.git
cd lvmh-risk-monitor
```

### 2. Install dependencies
```bash
pip install pandas matplotlib pytest
```

### 3. Run the main program
Open `main.ipynb` in VS Code or Jupyter and run all cells.

### 4. Run tests
```bash
python -m pytest tests/test_project.py -v
