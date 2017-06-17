import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

def dateparse(x):
	try:
		x = pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
		return x
	except ValueError as v:
		print "Error parsing date for " + x

# Instead of reading many keys from S3, we are able to roll up the data into csv files using Athena.
def load():
	df1 = pd.read_csv("../data/BTC-prices.csv", parse_dates=['last_updated'], date_parser=dateparse)
	df2 = pd.read_csv("../data/ETHER-prices.csv", parse_dates=['last_updated'], date_parser=dateparse)
	frames = [df1, df2]
	df = pd.concat(frames)
	df = df.set_index('last_updated')
	return df

def plot_logic(df):
	df1 = df[df['name'].str.contains('Bitcoin')]
	df2 = df[df['name'].str.contains('Ethereum')]
	plot(df1)

def plot(df):
	ax = df['price_usd'].plot(grid=True)
	ax.xaxis.set_label_text("date")
	plt.show()

def main():
	df = load()
	plot_logic(df)

if __name__ == "__main__":
    main()
