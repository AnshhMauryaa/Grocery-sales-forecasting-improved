import pandas as pd
import numpy as np

from prophet import Prophet

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


# ==================================================
# FORECAST FUTURE SALES
# ==================================================

def predict_next_months(df, product_name, months):
    """
    Predict future sales for a given product
    using Facebook Prophet
    """

    # Convert date column
    df["date_of_purchase"] = pd.to_datetime(
        df["date_of_purchase"],
        dayfirst=True,
        errors="coerce"
    )

    # Filter product
    product_df = df[
        df["product_name"].str.lower()
        == product_name.lower()
    ]

    if product_df.empty:
        raise ValueError(
            f"No data found for product: {product_name}"
        )

    # Aggregate daily sales
    daily_sales = (
        product_df
        .groupby("date_of_purchase")["quantity"]
        .sum()
        .reset_index()
    )

    # Prophet format
    prophet_df = daily_sales.rename(
        columns={
            "date_of_purchase": "ds",
            "quantity": "y"
        }
    )

    prophet_df = prophet_df.dropna()

    if len(prophet_df) < 2:
        raise ValueError(
            "Not enough historical data for forecasting."
        )

    # Create model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    # Train model
    model.fit(prophet_df)

    # Future dates
    future = model.make_future_dataframe(
        periods=months,
        freq="M"
    )

    # Forecast
    forecast = model.predict(future)

    # Extract future predictions
    result = forecast[
        ["ds", "yhat"]
    ].tail(months)

    result.rename(
        columns={
            "ds": "month",
            "yhat": "predicted_quantity"
        },
        inplace=True
    )

    result["predicted_quantity"] = (
        result["predicted_quantity"]
        .round(0)
        .astype(int)
    )

    return result


# ==================================================
# MODEL EVALUATION
# ==================================================

def evaluate_model(df, product_name):
    """
    Evaluate model performance
    using train-test split

    Returns:
    MAE
    RMSE
    MAPE
    Accuracy
    """

    # Convert date column
    df["date_of_purchase"] = pd.to_datetime(
        df["date_of_purchase"],
        dayfirst=True,
        errors="coerce"
    )

    # Filter selected product
    product_df = df[
        df["product_name"].str.lower()
        == product_name.lower()
    ]

    if product_df.empty:
        raise ValueError(
            f"No data found for product: {product_name}"
        )

    # Aggregate daily sales
    daily_sales = (
        product_df
        .groupby("date_of_purchase")["quantity"]
        .sum()
        .reset_index()
    )

    prophet_df = daily_sales.rename(
        columns={
            "date_of_purchase": "ds",
            "quantity": "y"
        }
    )

    prophet_df = prophet_df.dropna()

    if len(prophet_df) < 10:
        raise ValueError(
            "Need at least 10 records "
            "to calculate metrics."
        )

    # --------------------------
    # Train/Test Split
    # --------------------------

    split_index = int(
        len(prophet_df) * 0.8
    )

    train = prophet_df.iloc[:split_index]
    test = prophet_df.iloc[split_index:]

    # Prophet model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model.fit(train)

    # Predict test period
    future = test[["ds"]]

    forecast = model.predict(future)

    actual = test["y"].values
    predicted = forecast["yhat"].values

    # --------------------------
    # Metrics
    # --------------------------

    mae = mean_absolute_error(
        actual,
        predicted
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predicted
        )
    )

    # Avoid divide-by-zero
    actual_non_zero = np.where(
        actual == 0,
        1,
        actual
    )

    mape = np.mean(
        np.abs(
            (actual - predicted)
            / actual_non_zero
        )
    ) * 100

    accuracy = 100 - mape

    return {
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "MAPE": round(mape, 2),
        "Accuracy": round(accuracy, 2)
    }