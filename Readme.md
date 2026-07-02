# 📈 Grocery Sales Forecasting System

A Flask-based web application that predicts future grocery product demand using **Facebook Prophet**. Upload a historical sales dataset, select a product, specify the forecast period, and generate interactive sales forecasts with downloadable results.

---

## ✨ Features

- 📂 Upload grocery sales dataset (CSV)
- 🛒 Automatically detects available products from the uploaded dataset
- 📅 Forecast sales for a user-defined number of months
- 📈 Interactive sales forecast visualization using Plotly
- 📊 View forecast results in tabular format
- 📥 Download forecast results as a CSV file
- 🌐 Responsive web interface built with Flask and Bootstrap

---

## 🛠️ Tech Stack

- Python
- Flask
- Pandas
- Facebook Prophet
- Plotly
- Bootstrap 5
- HTML5 & CSS3

---

## 📂 Project Structure

```text
grocery-sales-forecast/
│
├── app.py                 # Flask application
├── forecast.py            # Forecasting logic
├── templates/
│   ├── landing.html
│   └── index.html
├── static/
├── forecast_output.csv
├── requirements.txt
└── README.md
```

---

## 🚀 Application Workflow

```text
Landing Page
      │
      ▼
Upload Grocery Sales Dataset
      │
      ▼
Dataset Validation & Product Extraction
      │
      ▼
Select Product
      │
      ▼
Enter Forecast Period
      │
      ▼
Generate Forecast
      │
      ▼
Interactive Chart + Forecast Table
      │
      ▼
Download Forecast CSV
```

---

## ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/grocery-sales-forecast.git
```

Navigate to the project directory:

```bash
cd grocery-sales-forecast
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask application:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## 📊 Output

- 📈 Interactive Forecast Graph
- 📋 Forecast Table
- 📥 Downloadable Forecast CSV

---

## 🔮 Future Enhancements

- Drag & Drop Dataset Upload
- Searchable Product Dropdown
- Dashboard Analytics
- Multiple Forecasting Models
- User Authentication
- Forecast History
- Inventory Recommendation System

---

## 👨‍💻 Author

Developed as a **Machine Learning & Data Science** project using **Flask**, **Facebook Prophet**, and **Plotly** to forecast grocery product demand through an intuitive web application.
