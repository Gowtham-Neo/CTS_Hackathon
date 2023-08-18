import pandas as pd

# Load the Nifty 50 dataset (replace with your data file)
data = pd.read_csv('E:\Hackathon\dataset.csv')
data.columns = data.columns.str.strip()
data['LTP'] = pd.to_numeric(data['LTP'], errors='coerce')
data['PREV. CLOSE'] = pd.to_numeric(data['PREV. CLOSE'], errors='coerce')
# Calculate percent changes from day 22 to day 23
data['percent_change_22_23'] = (data['LTP'] - data['PREV. CLOSE']) / data['PREV. CLOSE'] * 100

# Define the user's investable amount
investable_amount = float(input("Enter your investable amount: "))

# Filter out stocks with negative percent change (indicating potential losses)
data_positive_changes = data[data['percent_change_22_23'] > 0]

# Sort stocks by percent change in descending order
sorted_stocks = data_positive_changes.sort_values(by='percent_change_22_23', ascending=False)

# Recommend stocks based on investable amount
recommended_stocks = []
total_investment = 0
for _, row in sorted_stocks.iterrows():
    if total_investment + row['LTP'] <= investable_amount:
        recommended_stocks.append(row['SYMBOL'])
        total_investment += row['LTP']

# Now, we will consider additional factors like PE ratio, PB ratio, EPS, and face value
# Define weights for each factor (you can adjust these weights based on importance)
weight_pe_ratio = 0.2
weight_pb_ratio = 0.2
weight_eps = 0.3
weight_face_value = 0.3

# Calculate a score for each recommended stock based on the factors
stock_scores = []
for stock in recommended_stocks:
    score = (
        weight_pe_ratio * data[data['SYMBOL'] == stock]['PE RATIO'] +
        weight_pb_ratio * data[data['SYMBOL'] == stock]['PB RATIO'] +
        weight_eps * data[data['SYMBOL'] == stock]['EPS'] +
        weight_face_value * data[data['SYMBOL'] == stock]['FACE VALUE']
    )
    stock_scores.append((stock, score.values[0]))

# Sort stocks by their scores in descending order
stock_scores.sort(key=lambda x: x[1], reverse=True)

# Display the best recommended stock based on scores
if stock_scores:
    for i in range(len(stock_scores)):
        best_stock = stock_scores[i][0]
        print(f"The best recommended stock is: {best_stock}")
else:
    print("No recommended stocks within the investable amount.")
