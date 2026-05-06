import pandas as pd

class DataLoader:
    """Load and preprocess data from CSV file. Include volume parsing, percentage conversion and chronological sorting"""
    def __init__(self,filepath:str):
        #initialize the loader and clean data, and report error if no csv were found
        try:
            self.df = pd.read_csv(filepath)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filepath} not found. ")
        
        self.filepath = filepath
        self.clean_data()

    def clean_data(self):
        #clean and preprocess csv data

        #parse date
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%m/%d/%Y')

        #convert to volume in case of K, M, B
        def parse_volume(x):
            x = str(x).strip()
            if x.endswith('K'):
                return float(x.replace('K', '')) * 1_000
            elif x.endswith('M'):
                return float(x.replace('M', '')) * 1_000_000
            else:
                return float(x)
        self.df["Volume"] = self.df["Vol."].apply(parse_volume)

        #convert percentage to decimal
        try:
            self.df['Change'] = self.df['Change %'].apply(lambda x : float(x.replace('%',''))/100)
        except Exception as e:
            raise ValueError(f"Faild to parse Change % colunm: {e}")

        #sort by date ascending and reset index
        self.df = self.df.sort_values('Date').reset_index(drop=True)

    def get_data(self):
        #return cleaned data
        return self.df

    def __str__(self):
        #return string representation of the data
        return (f"MarketDataLoader for file: {self.filepath}\n"
                f"Rows: {len(self.df)}\n"
                f"Date range: {self.df['Date'].min()} to {self.df['Date'].max()}\n")

    def __len__(self):
        #return number of rows in the data
        return len(self.df)

if __name__ == "__main__":
    loader = DataLoader('Louis Vuitton Stock Price History.csv')
    print(loader)
    print(f"\nTotal records: {len(loader)}")
    print(loader.get_data().head())
