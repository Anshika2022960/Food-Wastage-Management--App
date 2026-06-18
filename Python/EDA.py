import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:Loria%402022@localhost:5432/Food_wastage_db"
)

providers = pd.read_sql("SELECT * FROM providers", engine)
receivers = pd.read_sql("SELECT * FROM receivers", engine)
food = pd.read_sql("SELECT * FROM food_listings", engine)
claims = pd.read_sql("SELECT * FROM claims", engine)

print(providers.head())
print(receivers.head())
print(food.head())
print(claims.head())


# 1.Univariate

# 1. Provider Type Distribution
plt.figure(figsize=(8,5))
sns.countplot(data=providers, x="type")
plt.title("Provider Type Distribution")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Receiver Type Distribution
plt.figure(figsize=(8,5))
sns.countplot(data=receivers, x="type")
plt.title("Receiver Type Distribution")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Food Type Distribution
plt.figure(figsize=(8,5))
sns.countplot(data=food, x="food_type")
plt.title("Food Type Distribution")
plt.tight_layout()
plt.show()

# 4. Meal Type Distribution
plt.figure(figsize=(8,5))
sns.countplot(data=food, x="meal_type")
plt.title("Meal Type Distribution")
plt.tight_layout()
plt.show()


# Bivariate

# 5. City vs Food Listings
city_food = food["location"].value_counts().head(10)
plt.figure(figsize=(10,5))
city_food.plot(kind="bar")
plt.title("Top 10 Cities by Food Listings")
plt.xlabel("City")
plt.ylabel("Number of Listings")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 6. Provider Type vs Quantity
provider_qty = food.groupby("provider_type")["quantity"].sum().sort_values(ascending=False)
plt.figure(figsize=(8,5))
provider_qty.plot(kind="bar")
plt.title("Provider Type vs Total Quantity")
plt.xlabel("Provider Type")
plt.ylabel("Total Quantity")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 7. Food Type vs Quantity
food_qty = food.groupby("food_type")["quantity"].sum().sort_values(ascending=False)
plt.figure(figsize=(8,5))
food_qty.plot(kind="bar")
plt.title("Food Type vs Total Quantity")
plt.xlabel("Food Type")
plt.ylabel("Total Quantity")
plt.tight_layout()
plt.show()

# 8. Meal Type vs Quantity
meal_qty = food.groupby("meal_type")["quantity"].sum().sort_values(ascending=False)
plt.figure(figsize=(8,5))
meal_qty.plot(kind="bar")
plt.title("Meal Type vs Total Quantity")
plt.xlabel("Meal Type")
plt.ylabel("Total Quantity")
plt.tight_layout()
plt.show()

# 9. City + Provider Type + Quantity
city_provider_qty = food.groupby(["location", "provider_type"])["quantity"].sum().reset_index()
top_city_provider = city_provider_qty.sort_values("quantity", ascending=False).head(15)

plt.figure(figsize=(12,6))
sns.barplot(data=top_city_provider, x="location", y="quantity", hue="provider_type")
plt.title("City + Provider Type + Quantity")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Multivariate

# 10. Food Type + Meal Type + Quantity
food_meal_qty = food.groupby(["food_type", "meal_type"])["quantity"].sum().reset_index()

plt.figure(figsize=(10,6))
sns.barplot(data=food_meal_qty, x="food_type", y="quantity", hue="meal_type")
plt.title("Food Type + Meal Type + Quantity")
plt.tight_layout()
plt.show()

# Merge data for claim-based analysis
claim_food = claims.merge(food, on="food_id", how="left")

# 11. Provider + Claims + Quantity
provider_claims = claim_food.groupby("provider_id").agg(
    total_claims=("claim_id", "count"),
    total_quantity=("quantity", "sum")
).reset_index().sort_values("total_claims", ascending=False).head(10)

plt.figure(figsize=(10,5))
sns.barplot(data=provider_claims, x="provider_id", y="total_claims")
plt.title("Top Providers by Claims")
plt.xlabel("Provider ID")
plt.ylabel("Total Claims")
plt.tight_layout()
plt.show()

# 12. Receiver + Claims + Quantity
receiver_claims = claim_food.groupby("receiver_id").agg(
    total_claims=("claim_id", "count"),
    total_quantity=("quantity", "sum")
).reset_index().sort_values("total_claims", ascending=False).head(10)

plt.figure(figsize=(10,5))
sns.barplot(data=receiver_claims, x="receiver_id", y="total_claims")
plt.title("Top Receivers by Claims")
plt.xlabel("Receiver ID")
plt.ylabel("Total Claims")
plt.tight_layout()
plt.show()


# Claim Analysis

# 13. Claim Status Distribution
plt.figure(figsize=(8,5))
sns.countplot(data=claims, x="status")
plt.title("Claim Status Distribution")
plt.tight_layout()
plt.show()

# 14. Top Receivers
top_receivers = claims["receiver_id"].value_counts().head(10)

plt.figure(figsize=(10,5))
top_receivers.plot(kind="bar")
plt.title("Top 10 Receivers by Number of Claims")
plt.xlabel("Receiver ID")
plt.ylabel("Claim Count")
plt.tight_layout()
plt.show()

# 15. Top Providers
top_providers = claim_food["provider_id"].value_counts().head(10)

plt.figure(figsize=(10,5))
top_providers.plot(kind="bar")
plt.title("Top 10 Providers by Number of Claims")
plt.xlabel("Provider ID")
plt.ylabel("Claim Count")
plt.tight_layout()
plt.show()