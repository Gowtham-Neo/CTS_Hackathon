from flask import Flask, render_template, request
import pandas as pd
import base64
import io
import threading
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('Agg')
from waitress import serve
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)
plot_lock = threading.Lock()

# Load the dataset
data = pd.read_csv("E:\PROJECTS\DNTechnoverse Hackathon\Testing\datasets\dataset.csv")
data.columns = data.columns.str.strip()
data["LTP"] = pd.to_numeric(data["LTP"], errors="coerce")
data["PREV. CLOSE"] = pd.to_numeric(data["PREV. CLOSE"], errors="coerce")
data["percent_change_22_23"] = (
    (data["LTP"] - data["PREV. CLOSE"]) / data["PREV. CLOSE"] * 100
)
data.dropna(subset=["LTP"], inplace=True)
# Select the features and target variable
features = data[["PE RATIO", "PB RATIO", "EPS", "FACE VALUE"]]
target = data["LTP"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Create and train the RandomForestRegressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

@app.route("/", methods=["GET", "POST"])
def recommend_stocks():
    if request.method == "POST":
        investable_amount = float(request.form.get("investable_amount"))

        # Use the trained model to predict stock prices
        predicted_prices = model.predict(features)

        # Combine predicted prices with stock symbols
        data["Predicted Price"] = predicted_prices
        data_positive_changes = data[data["Predicted Price"] > data["LTP"]]

        # Sort the stocks by predicted price change and select recommended stocks
        sorted_stocks = data_positive_changes.sort_values(
            by="Predicted Price", ascending=False
        )
        recommended_stocks = []
        total_investment = 0
        for _, row in sorted_stocks.iterrows():
            if total_investment + row["LTP"] <= investable_amount:
                recommended_stocks.append(row["SYMBOL"])
                total_investment += row["LTP"]

        # Render the results template and pass the recommended stocks as variables
        return render_template("results.html", best_stocks=recommended_stocks)

    return render_template("index.html")

@app.route("/symbol/<symbol>")
def show_stock_details(symbol):
    stock_metrics = data[data["SYMBOL"] == symbol]

    file_path = f"datasets/{symbol}.csv"
    stock_data = pd.read_csv(file_path)

    # Filter stock_data for the date range (2020 to 2021)
    stock_data = stock_data[
        (stock_data["Date"] >= "2020-01-01") & (stock_data["Date"] <= "2021-12-31")
    ]
    stock_data["Date"] = pd.to_datetime(stock_data["Date"])

    # Filter the data to include only the first day of each month in 2020 and 2021
    filtered_data = stock_data[
        (stock_data["Date"].dt.year.isin([2020, 2021]))
        & (stock_data["Date"].dt.day == 1)
    ]

    # Prepare data for the graph
    graph_labels = filtered_data["Date"].dt.strftime("%b %Y")  # Format: Jan 2020
    graph_data = filtered_data["Last"]

    plt.figure(figsize=(10, 6))
    plt.plot(stock_data["Date"], stock_data["Last"], label="Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"{symbol} Stock Price (2020-2021)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    plot_img = base64.b64encode(img_buffer.read()).decode("utf-8")

    return render_template(
        "symbol_details.html",
        symbol=symbol,
        plot_img=plot_img,
        pe_ratio=stock_metrics["PE RATIO"].values[0],
        pb_ratio=stock_metrics["PB RATIO"].values[0],
        eps=stock_metrics["EPS"].values[0],
        Div=stock_metrics["DIV YIELD"].values[0],
        Mcap=stock_metrics["MCAP"].values[0],
        Face_value=stock_metrics["FACE VALUE"].values[0],
        raph_labels=graph_labels.tolist(),  # Convert to list
        graph_data=graph_data.tolist(),  # Convert to list
        stock_data=filtered_data.to_dict(orient="records"),
    )


if __name__ == "__main__":

    serve(app,host="0.0.0.0",port=8080)
