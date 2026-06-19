# ♻️ Local Food Wastage Management System

## 📌 Project Overview

The **Local Food Wastage Management System** is a data-driven application developed using **Streamlit** and **PostgreSQL** to help reduce food wastage by connecting food providers with receivers.

The system enables users to explore food availability, analyze donation trends, track food claims, and manage food listings through CRUD operations.

---

## 🎯 Project Objectives

* Minimize food wastage through efficient food redistribution.
* Connect food providers with receivers and NGOs.
* Monitor food availability and demand across different cities.
* Analyze food donation and claim trends using SQL queries and EDA.
* Provide actionable business insights through interactive dashboards.

---

## 🛠️ Technologies Used

* Python
* Streamlit
* PostgreSQL
* SQLAlchemy
* Pandas
* Plotly Express
* Pillow

---

## 🗄️ Database Tables

The application uses the following tables:

* `food_listings`
* `providers`
* `receivers`
* `claims`

---

## ✨ Features

### 🔍 Filter Options

* Filter by City
* Filter by Provider Type
* Filter by Meal Type
* Filter by Food Type

### 📊 Dashboard KPIs

* Total Food Quantity Available
* Total Food Listings
* Total Providers
* Total Receivers
* Total Claims
* Claim Completion Rate
* Average Quantity per Listing
* Food Recovery Rate
* Expiring Food Count

### 📈 SQL Analysis

* Execute 15+ SQL queries for business insights.

### 📉 Exploratory Data Analysis (EDA)

* 15 interactive charts for food donation and claim analysis.

### 📞 Contact Information

* Provider Contact Information
* Receiver Contact Information

### 🤝 Food Claims

* Submit food claims directly through the application.

### 📝 CRUD Operations

* Add new food listings
* Update food quantities
* Delete food listings
* View all records

### ⬇️ Data Export

* Download filtered food listings as CSV.

---

## 💡 Business Insights

The application helps answer questions such as:

* Which city has the highest food availability?
* Which meal type gets wasted the most?
* Which provider contributes the most food?
* Which receiver claims the most food?
* What percentage of claims are completed?
* Which city has the highest food demand?

---

## 🚀 Business Recommendations

* Increase NGO partnerships in high food-wastage cities.
* Recognize top food providers for their contributions.
* Send automated notifications before food expiry.
* Increase collection efforts in high-demand locations.

---

## ▶️ How to Run the Application

### Step 1: Clone the repository

```bash
git clone <repository-link>
cd <repository-folder>
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure the database connection

Update the database credentials in `database.py`.

### Step 4: Run the application
streamlit run app.py

### step 5: Streamlit Live Demo URL [https://food-wastage-management--app.streamlit.app/]

```bash





```

---

## 📷 Screenshots

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Food Listings

![Food Listings](screenshots/food_listings.png)

### Contact Information

![Contact Information](screenshots/contacts.png)

### SQL Analysis

![SQL Analysis](screenshots/sql_analysis.png)

### EDA Charts

![EDA Charts](screenshots/eda_charts.png)

### Food Claims

![Food Claims](screenshots/food_claims.png)

### CRUD Operations

![CRUD Operations](screenshots/crud_operations.png)
