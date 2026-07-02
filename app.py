from flask import Flask, render_template, request, send_file
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

from forecast import predict_next_months

app = Flask(__name__)

# Store uploaded dataframe
uploaded_df = None

# Save forecast output
forecast_file = "forecast_output.csv"


# -----------------------------
# Landing Page
# -----------------------------
@app.route("/")
def home():
    return render_template("landing.html")


# -----------------------------
# Upload Page
# -----------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():

    global uploaded_df

    # First time opening page
    if request.method == "GET":
        return render_template(
            "index.html",
            uploaded=False
        )

    try:

        file = request.files["file"]

        if file.filename == "":
            raise ValueError("Please select a CSV file.")

        # Read CSV
        uploaded_df = pd.read_csv(file)

        # Product list
        products = sorted(
            uploaded_df["product_name"]
            .dropna()
            .unique()
            .tolist()
        )

        return render_template(
            "index.html",
            uploaded=True,
            upload_success=True,
            filename=file.filename,
            rows=len(uploaded_df),
            total_products=len(products),
            products=products
        )

    except Exception as e:

        return render_template(
            "index.html",
            uploaded=False,
            error=str(e)
        )


# -----------------------------
# Generate Forecast
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    global uploaded_df

    try:

        if uploaded_df is None:
            raise ValueError("Please upload a dataset first.")

        product_name = request.form["product_name"]
        months = int(request.form["months"])

        result = predict_next_months(
            uploaded_df,
            product_name,
            months
        )

        result.to_csv(
            forecast_file,
            index=False
        )

        fig = px.line(
            result,
            x="month",
            y="predicted_quantity",
            markers=True,
            title=f"{product_name} Sales Forecast"
        )

        graph_html = pio.to_html(
            fig,
            full_html=False
        )

        table = result.to_html(
            classes="table table-striped",
            index=False
        )

        products = sorted(
            uploaded_df["product_name"]
            .dropna()
            .unique()
            .tolist()
        )

        return render_template(
            "index.html",
            uploaded=True,
            upload_success=True,
            filename="Dataset Uploaded",
            rows=len(uploaded_df),
            total_products=len(products),
            products=products,
            graph_html=graph_html,
            table=table,
            success=True
        )

    except Exception as e:

        products = []

        if uploaded_df is not None:

            products = sorted(
                uploaded_df["product_name"]
                .dropna()
                .unique()
                .tolist()
            )

            return render_template(
                "index.html",
                uploaded=True,
                upload_success=True,
                filename="Dataset Uploaded",
                rows=len(uploaded_df),
                total_products=len(products),
                products=products,
                error=str(e)
            )

        return render_template(
            "index.html",
            uploaded=False,
            error=str(e)
        )


# -----------------------------
# Download Forecast
# -----------------------------
@app.route("/download")
def download():

    if os.path.exists(forecast_file):
        return send_file(
            forecast_file,
            as_attachment=True
        )

    return "Forecast file not found."


if __name__ == "__main__":
    app.run(debug=True)