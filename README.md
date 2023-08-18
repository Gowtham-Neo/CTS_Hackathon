# EquityVision - Stock Recommendation System

EquityVision is a stock recommendation system that assists users in making informed investment choices by offering personalized stock recommendations based on their investable amount. The system utilizes machine learning techniques to forecast stock price changes and propose stocks with potential positive price changes.

## Project Overview

This project consists of four main parts:

1. `app.py`: Flask web application serving as the user interface and handling user input for the investable amount and also
Contains the machine learning model for predicting stock price changes.
2. `datasets`:Directory containing all the datasets of nifty-50 stocks in csv format
3. `templates/`: Directory containing HTML templates for the user interface.
4. `static/`: Directory containing static image for this project

## Prerequisites

Before you run the project, make sure you have the following installed:

- Python 3.x

You also need to install the required libraries using the following commands:

```bash
pip install flask pandas scikit-learn matplotlib
  ```
  or
  
## Prerequisites

Before running the project, ensure you have the following dependencies installed:

- Python (3.6 or higher)
- Flask (install with `pip install Flask`)
- Pandas (install with `pip install pandas`)
- Scikit-learn (install with `pip install scikit-learn`)
- Matplotlib (install with `pip install matplotlib`)
- Waitress (install with `pip install waitress`)
  
How to Use
1.Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/equityvision.git
 ```
2.Navigate to the project directory:
```bash
cd
  ```
3.You also need to install the required libraries using the following commands:

```bash
pip install flask pandas scikit-learn matplotlib
  ```
  or
  ## Prerequisites

Before running the project, ensure you have the following dependencies installed:

- Python (3.6 or higher)
- Flask (install with `pip install Flask`)
- Pandas (install with `pip install pandas`)
- Scikit-learn (install with `pip install scikit-learn`)
- Matplotlib (install with `pip install matplotlib`)
- Waitress (install with `pip install waitress`)
  
4.Run the Flask app:
```bash
python index.py
  ```
5.Open a web browser and navigate to http://localhost:8080 to access the EquityVision application.
```bash
http://localhost:8080
```
You should be able to view the homepage.

Enter valid numerical investable amount to get the recommended stocks then after clicking each stock you will be able
see key metrics and graph from 2020 to 2021



