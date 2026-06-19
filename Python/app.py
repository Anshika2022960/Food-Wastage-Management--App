from PIL import Image
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Local Food Wastage Management System",
    page_icon="♻️",
    layout="wide"
)

st.markdown("""
<style>
/* Main dashboard background */
[data-testid="stAppViewContainer"] {
    background-color: #18202B;
}

/* Sidebar background - matching but slightly darker */
[data-testid="stSidebar"] {
    background-color: #18202B;
}

/* Main content text */
h1, h2, h3, p, label, span {
    color: #F5F7FA !important;
}

/* Sidebar labels */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #F5F7FA !important;
    font-weight: 600;
}

/* Dropdown boxes */
[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border-radius: 8px;
}

/* KPI cards */
[data-testid="stMetric"] {
    background-color: #243247;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #3A4A63;
}

/* KPI title */
[data-testid="stMetricLabel"] {
    color: #E6EDF5 !important;
}

/* KPI value */
[data-testid="stMetricValue"] {
    color: #2EE6C8 !important;
    font-size: 32px;
}

/* Divider */
hr {
    border: 1px solid #3A4A63;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
try:
    banner = Image.open("banner.png")
    col1, col2 = st.columns([1, 5])

    with col1:
        st.markdown("<div style='margin-top:50px;'>", unsafe_allow_html=True)
        st.image(banner, width=120)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <h1 style='font-size:30px; margin-top:35px; margin-left:-40px;'>
            Local Food Wastage Management System
        </h1>
        """, unsafe_allow_html=True)

except:
    st.title("♻️ Local Food Wastage Management System")

st.markdown("---")

# ---------------- LOAD DATA ----------------

food = pd.read_csv("Raw Data/food_listings_data.csv")
providers = pd.read_csv("Raw Data/providers_data.csv")
receivers = pd.read_csv("Raw Data/receivers_data.csv")
claims = pd.read_csv("Raw Data/claims_data.csv")

# Clean column names
food.columns = food.columns.str.strip().str.lower()
providers.columns = providers.columns.str.strip().str.lower()
receivers.columns = receivers.columns.str.strip().str.lower()
claims.columns = claims.columns.str.strip().str.lower()



# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filter Options")

city = st.sidebar.multiselect("Select City", options=sorted(food["location"].dropna().unique()))
provider = st.sidebar.multiselect("Select Provider Type", options=sorted(food["provider_type"].dropna().unique()))
meal = st.sidebar.multiselect("Select Meal Type", options=sorted(food["meal_type"].dropna().unique()))
food_type = st.sidebar.multiselect("Select Food Type", options=sorted(food["food_type"].dropna().unique()))

filtered_food = food.copy()

if city:
    filtered_food = filtered_food[filtered_food["location"].isin(city)]
if provider:
    filtered_food = filtered_food[filtered_food["provider_type"].isin(provider)]
if meal:
    filtered_food = filtered_food[filtered_food["meal_type"].isin(meal)]
if food_type:
    filtered_food = filtered_food[filtered_food["food_type"].isin(food_type)]

# ---------------- 9 KPIs ----------------
st.markdown("## 📊 Executive Dashboard")
st.caption("Real-time food donation, claim, provider and recovery analysis")

total_food_quantity = int(filtered_food["quantity"].sum())
total_food_listings = len(filtered_food)
total_providers = providers["provider_id"].nunique()
total_receivers = receivers["receiver_id"].nunique()
total_claims = len(claims)

completed_claims = len(claims[claims["status"] == "Completed"])
claim_completion_rate = round((completed_claims / total_claims) * 100, 2) if total_claims > 0 else 0

avg_quantity = round(filtered_food["quantity"].mean(), 2) if len(filtered_food) > 0 else 0
food_recovery_rate = claim_completion_rate

filtered_food["expiry_date"] = pd.to_datetime(filtered_food["expiry_date"])
today = pd.Timestamp.today().normalize()

expiring_food_count = len(
    filtered_food[
        (filtered_food["expiry_date"] >= today) &
        (filtered_food["expiry_date"] <= today + pd.Timedelta(days=3))
    ]
)

k1, k2, k3 = st.columns(3)
k1.metric("Total Food Quantity Available", total_food_quantity)
k2.metric("Total Food Listings", total_food_listings)
k3.metric("Total Providers", total_providers)

k4, k5, k6 = st.columns(3)
k4.metric("Total Receivers", total_receivers)
k5.metric("Total Claims", total_claims)
k6.metric("Claim Completion Rate (%)", f"{claim_completion_rate}%")

k7, k8, k9 = st.columns(3)
k7.metric("Average Quantity per Listing", avg_quantity)
k8.metric("Food Recovery Rate (%)", f"{food_recovery_rate}%")
k9.metric("Expiring Food Count", expiring_food_count)

st.markdown("---")
st.subheader("📈 Key Visual Insights")

c1, c2 = st.columns(2)

with c1:
    chart_data = food.groupby("provider_type")["quantity"].sum().reset_index()
    fig = px.bar(chart_data, x="provider_type", y="quantity",
                 title="Food Quantity by Provider Type")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    claim_data = claims["status"].value_counts().reset_index()
    claim_data.columns = ["status", "count"]
    fig = px.pie(claim_data, names="status", values="count",
                 title="Claim Status Distribution")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    city_data = food["location"].value_counts().head(10).reset_index()
    city_data.columns = ["location", "count"]
    fig = px.bar(city_data, x="location", y="count",
                 title="Top Cities by Food Listings")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    meal_data = food.groupby("meal_type")["quantity"].sum().reset_index()
    fig = px.bar(meal_data, x="meal_type", y="quantity",
                 title="Meal Type vs Quantity")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- FOOD LISTINGS TABLE ----------------

st.markdown("---")

st.subheader("🍱 Food Listings Data")
st.dataframe(filtered_food, use_container_width=True)

csv = filtered_food.to_csv(index=False)
st.download_button(
    "Download Filtered CSV",
    csv,
    "food_listings.csv",
    "text/csv"
)

# ---------------- CONTACT INFORMATION ----------------
st.markdown("---")
st.subheader("📞 Provider Contact Information")
provider_contact = providers[["name", "type", "address", "city", "contact"]]
st.dataframe(provider_contact, use_container_width=True)

st.markdown("---")
st.subheader("📞 Receiver Contact Information")
receiver_contact = receivers[["name", "type", "city", "contact"]]
st.dataframe(receiver_contact, use_container_width=True)

# ---------------- SQL ANALYSIS ----------------
st.markdown("---")
st.subheader("📊 SQL Analysis")

sql_queries = {
    "1. Providers by City": """
        SELECT city, COUNT(*) AS total_providers
        FROM providers
        GROUP BY city
        ORDER BY total_providers DESC;
    """,

    "2. Receivers by City": """
        SELECT city, COUNT(*) AS total_receivers
        FROM receivers
        GROUP BY city
        ORDER BY total_receivers DESC;
    """,

    "3. Most Contributing Provider Type": """
        SELECT provider_type, SUM(quantity) AS total_quantity
        FROM food_listings
        GROUP BY provider_type
        ORDER BY total_quantity DESC;
    """,

    "4. Most Claimed Food": """
        SELECT f.food_name, COUNT(c.claim_id) AS total_claims
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        GROUP BY f.food_name
        ORDER BY total_claims DESC;
    """,

    "5. Total Food Quantity": """
        SELECT SUM(quantity) AS total_food_quantity
        FROM food_listings;
    """,

    "6. Top City by Food Listing": """
        SELECT location, COUNT(*) AS total_food_listings
        FROM food_listings
        GROUP BY location
        ORDER BY total_food_listings DESC;
    """,

    "7. Most Common Food Type": """
        SELECT food_type, COUNT(*) AS total_count
        FROM food_listings
        GROUP BY food_type
        ORDER BY total_count DESC;
    """,

    "8. Claims per Food Item": """
        SELECT f.food_name, COUNT(c.claim_id) AS total_claims
        FROM food_listings f
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY f.food_name
        ORDER BY total_claims DESC;
    """,

    "9. Provider with Most Successful Claims": """
        SELECT p.name AS provider_name, COUNT(c.claim_id) AS successful_claims
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        JOIN providers p ON f.provider_id = p.provider_id
        WHERE c.status = 'Completed'
        GROUP BY p.name
        ORDER BY successful_claims DESC;
    """,

    "10. Claim Status Percentage": """
        SELECT status,
               COUNT(*) AS total_claims,
               ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
        FROM claims
        GROUP BY status
        ORDER BY percentage DESC;
    """,

    "11. Average Quantity Claimed": """
        SELECT ROUND(AVG(f.quantity), 2) AS average_quantity_claimed
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id;
    """,

    "12. Most Claimed Meal Type": """
        SELECT f.meal_type, COUNT(c.claim_id) AS total_claims
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        GROUP BY f.meal_type
        ORDER BY total_claims DESC;
    """,

    "13. Total Donated Quantity by Provider": """
        SELECT p.name AS provider_name, SUM(f.quantity) AS total_donated_quantity
        FROM providers p
        JOIN food_listings f ON p.provider_id = f.provider_id
        GROUP BY p.name
        ORDER BY total_donated_quantity DESC;
    """,

    "14. Food Nearing Expiry": """
        SELECT food_name, quantity, expiry_date, location
        FROM food_listings
        WHERE expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '3 days'
        ORDER BY expiry_date;
    """,

    "15. City with Highest Completed Claims": """
        SELECT f.location, COUNT(c.claim_id) AS completed_claims
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        WHERE c.status = 'Completed'
        GROUP BY f.location
        ORDER BY completed_claims DESC;
    """
}

query_option = st.selectbox("Select SQL Query", list(sql_queries.keys()))
st.info("SQL queries are included in the project SQL file. Live deployed version uses CSV data for dashboard and EDA.")


# ---------------- EDA CHARTS ----------------
st.markdown("---")
st.subheader("📈 EDA Charts")

chart_option = st.selectbox(
    "Select EDA Chart",
    [
        "1. Provider Type Distribution",
        "2. Receiver Type Distribution",
        "3. Food Type Distribution",
        "4. Meal Type Distribution",
        "5. City vs Food Listings",
        "6. Provider Type vs Quantity",
        "7. Food Type vs Quantity",
        "8. Meal Type vs Quantity",
        "9. City + Provider Type + Quantity",
        "10. Food Type + Meal Type + Quantity",
        "11. Provider + Claims + Quantity",
        "12. Receiver + Claims + Quantity",
        "13. Claim Status Distribution",
        "14. Top Receivers",
        "15. Top Providers"
    ]
)

if chart_option == "1. Provider Type Distribution":
    chart_data = providers["type"].value_counts().reset_index()
    chart_data.columns = ["type", "count"]
    fig = px.bar(chart_data, x="type", y="count", title="Provider Type Distribution")

elif chart_option == "2. Receiver Type Distribution":
    chart_data = receivers["type"].value_counts().reset_index()
    chart_data.columns = ["type", "count"]
    fig = px.bar(chart_data, x="type", y="count", title="Receiver Type Distribution")

elif chart_option == "3. Food Type Distribution":
    chart_data = food["food_type"].value_counts().reset_index()
    chart_data.columns = ["food_type", "count"]
    fig = px.pie(chart_data, names="food_type", values="count", title="Food Type Distribution")

elif chart_option == "4. Meal Type Distribution":
    chart_data = food["meal_type"].value_counts().reset_index()
    chart_data.columns = ["meal_type", "count"]
    fig = px.bar(chart_data, x="meal_type", y="count", title="Meal Type Distribution")

elif chart_option == "5. City vs Food Listings":
    chart_data = food["location"].value_counts().head(10).reset_index()
    chart_data.columns = ["location", "count"]
    fig = px.bar(chart_data, x="location", y="count", title="City vs Food Listings")

elif chart_option == "6. Provider Type vs Quantity":
    chart_data = food.groupby("provider_type")["quantity"].sum().reset_index()
    fig = px.bar(chart_data, x="provider_type", y="quantity", title="Provider Type vs Quantity")

elif chart_option == "7. Food Type vs Quantity":
    chart_data = food.groupby("food_type")["quantity"].sum().reset_index()
    fig = px.bar(chart_data, x="food_type", y="quantity", title="Food Type vs Quantity")

elif chart_option == "8. Meal Type vs Quantity":
    chart_data = food.groupby("meal_type")["quantity"].sum().reset_index()
    fig = px.bar(chart_data, x="meal_type", y="quantity", title="Meal Type vs Quantity")

elif chart_option == "9. City + Provider Type + Quantity":
    chart_data = food.groupby(["location", "provider_type"])["quantity"].sum().reset_index().head(20)
    fig = px.bar(chart_data, x="location", y="quantity", color="provider_type", title="City + Provider Type + Quantity")

elif chart_option == "10. Food Type + Meal Type + Quantity":
    chart_data = food.groupby(["food_type", "meal_type"])["quantity"].sum().reset_index()
    fig = px.bar(chart_data, x="food_type", y="quantity", color="meal_type", title="Food Type + Meal Type + Quantity")

elif chart_option == "11. Provider + Claims + Quantity":
    claim_food = claims.merge(food, on="food_id", how="left")
    chart_data = claim_food.groupby("provider_id").agg(
        total_claims=("claim_id", "count"),
        total_quantity=("quantity", "sum")
    ).reset_index().sort_values("total_claims", ascending=False).head(10)
    fig = px.bar(chart_data, x="provider_id", y="total_claims", title="Provider + Claims + Quantity")

elif chart_option == "12. Receiver + Claims + Quantity":
    claim_food = claims.merge(food, on="food_id", how="left")
    chart_data = claim_food.groupby("receiver_id").agg(
        total_claims=("claim_id", "count"),
        total_quantity=("quantity", "sum")
    ).reset_index().sort_values("total_claims", ascending=False).head(10)
    fig = px.bar(chart_data, x="receiver_id", y="total_claims", title="Receiver + Claims + Quantity")

elif chart_option == "13. Claim Status Distribution":
    chart_data = claims["status"].value_counts().reset_index()
    chart_data.columns = ["status", "count"]
    fig = px.pie(chart_data, names="status", values="count", title="Claim Status Distribution")

elif chart_option == "14. Top Receivers":
    chart_data = claims["receiver_id"].value_counts().head(10).reset_index()
    chart_data.columns = ["receiver_id", "claim_count"]
    fig = px.bar(chart_data, x="receiver_id", y="claim_count", title="Top Receivers")

elif chart_option == "15. Top Providers":
    claim_food = claims.merge(food, on="food_id", how="left")
    chart_data = claim_food["provider_id"].value_counts().head(10).reset_index()
    chart_data.columns = ["provider_id", "claim_count"]
    fig = px.bar(chart_data, x="provider_id", y="claim_count", title="Top Providers")

st.plotly_chart(fig, use_container_width=True)

# ---------------- FOOD CLAIM ----------------
st.markdown("---")
st.subheader("🤝 Food Claim")

with st.expander("Claim Food"):
    st.dataframe(food[["food_id", "food_name", "quantity", "location", "meal_type"]].head(20))

    claim_food_id = st.number_input("Food ID to Claim", min_value=1, step=1)
    receiver_id = st.number_input("Receiver ID", min_value=1, step=1)
    claim_status = st.selectbox("Claim Status", ["Pending", "Completed", "Cancelled"])

    if st.button("Submit Claim"):
        try:
            max_claim = pd.read_sql("SELECT COALESCE(MAX(claim_id), 0) + 1 AS new_id FROM claims", engine)
            new_claim_id = int(max_claim["new_id"][0])

            query = """
            INSERT INTO claims
            (claim_id, food_id, receiver_id, status, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """

            conn = engine.raw_connection()
            cur = conn.cursor()
            cur.execute(query, (new_claim_id, claim_food_id, receiver_id, claim_status, datetime.now()))
            conn.commit()
            cur.close()
            conn.close()

            st.success("Food claim submitted successfully!")

        except Exception as e:
            st.error(f"Error while submitting claim: {e}")

# ---------------- CRUD OPERATIONS ----------------
st.markdown("---")
st.subheader("📝 CRUD Operations")

crud_option = st.selectbox(
    "Choose Operation",
    ["View Records", "Add Food Listing", "Update Food Quantity", "Delete Food Listing"]
)

if crud_option == "View Records":
    st.warning("Food Claim and CRUD operations are available in the local PostgreSQL version. The deployed version is read-only CSV demo.")

elif crud_option == "Add Food Listing":
    food_id = st.number_input("Food ID", min_value=1, step=1)
    food_name = st.text_input("Food Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    expiry_date = st.date_input("Expiry Date")
    provider_id = st.number_input("Provider ID", min_value=1, step=1)
    provider_type = st.text_input("Provider Type")
    location = st.text_input("Location")
    food_type_input = st.selectbox("Food Type for New Record", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    meal_type_input = st.selectbox("Meal Type for New Record", ["Breakfast", "Lunch", "Dinner", "Snacks"])

    if st.button("Add Record"):
        try:
            query = """
            INSERT INTO food_listings
            (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            conn = engine.raw_connection()
            cur = conn.cursor()

            cur.execute(query, (
                food_id,
                food_name,
                quantity,
                expiry_date,
                provider_id,
                provider_type,
                location,
                food_type_input,
                meal_type_input
            ))

            conn.commit()
            cur.close()
            conn.close()

            st.success("Food listing added successfully!")

        except Exception as e:
            st.error(f"Error while adding record: {e}")

elif crud_option == "Update Food Quantity":
    update_food_id = st.number_input("Enter Food ID to Update", min_value=1, step=1)
    new_quantity = st.number_input("New Quantity", min_value=0, step=1)

    if st.button("Update Record"):
        try:
            query = """
            UPDATE food_listings
            SET quantity = %s
            WHERE food_id = %s
            """

            conn = engine.raw_connection()
            cur = conn.cursor()
            cur.execute(query, (new_quantity, update_food_id))
            conn.commit()
            cur.close()
            conn.close()

            st.success("Food quantity updated successfully!")

        except Exception as e:
            st.error(f"Error while updating record: {e}")

elif crud_option == "Delete Food Listing":
    delete_food_id = st.number_input("Enter Food ID to Delete", min_value=1, step=1)

    if st.button("Delete Record"):
        try:
            query = """
            DELETE FROM food_listings
            WHERE food_id = %s
            """

            conn = engine.raw_connection()
            cur = conn.cursor()
            cur.execute(query, (delete_food_id,))
            conn.commit()
            cur.close()
            conn.close()

            st.success("Food listing deleted successfully!")

        except Exception as e:
            st.error(f"Error while deleting record: {e}")