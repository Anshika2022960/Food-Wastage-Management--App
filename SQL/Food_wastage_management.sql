----------------------------- Phase - 1----------------------------------------
SET datestyle = 'MDY';

CREATE TABLE providers (
    provider_id INT PRIMARY KEY,
    name VARCHAR(100),
    type VARCHAR(50),
    address TEXT,
    city VARCHAR(50),
    contact VARCHAR(50)
);

CREATE TABLE receivers (
    receiver_id INT PRIMARY KEY,
    name VARCHAR(100),
    type VARCHAR(50),
    city VARCHAR(50),
    contact VARCHAR(50)
);

CREATE TABLE food_listings (
    food_id INT PRIMARY KEY,
    food_name VARCHAR(100),
    quantity INT,
    expiry_date DATE,
    provider_id INT,
    provider_type VARCHAR(50),
    location VARCHAR(50),
    food_type VARCHAR(50),
    meal_type VARCHAR(50),
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id)
);

CREATE TABLE claims (
    claim_id INT PRIMARY KEY,
    food_id INT,
    receiver_id INT,
    status VARCHAR(30),
    timestamp TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES food_listings(food_id),
    FOREIGN KEY (receiver_id) REFERENCES receivers(receiver_id)
);


SELECT * FROM providers;
SELECT * FROM receivers;
SELECT * FROM food_listings;
SELECT * FROM claims;




SELECT COUNT(*) FROM claims;
SELECT * FROM claims LIMIT 5;


------------------ Phase 2: Checking Null Values -----------------------------

-------Providers table-----
SELECT *
FROM providers
WHERE contact IS NULL
   OR address IS NULL;

SELECT
COUNT(*) FILTER (WHERE contact IS NULL) AS missing_contact,
COUNT(*) FILTER (WHERE address IS NULL) AS missing_address
FROM providers;

-------- Receivers ----------

SELECT COUNT(*) FILTER (WHERE contact IS NULL) AS missing_contact
FROM receivers;

-------- Food Listings --------

SELECT
COUNT(*) FILTER (WHERE expiry_date IS NULL) AS missing_expiry,
COUNT(*) FILTER (WHERE quantity IS NULL) AS missing_quantity
FROM food_listings;

---------  Claims ---------

SELECT
COUNT(*) FILTER (WHERE status IS NULL) AS missing_status,
COUNT(*) FILTER (WHERE timestamp IS NULL) AS missing_timestamp
FROM claims;



SELECT COUNT(*) FROM providers WHERE contact IS NULL OR address IS NULL;

SELECT COUNT(*) FROM receivers WHERE contact IS NULL;

SELECT COUNT(*) FROM food_listings
WHERE expiry_date IS NULL OR quantity IS NULL;

SELECT COUNT(*) FROM claims
WHERE status IS NULL OR timestamp IS NULL;


------------- 15 SQL analysis queries -----------------

----1. Providers by city----

SELECT city, COUNT(*) AS total_providers
FROM providers
GROUP BY city
ORDER BY total_providers DESC;

---- 2. Receivers by city----

SELECT city, COUNT(*) AS total_receivers
FROM receivers
GROUP BY city
ORDER BY total_receivers DESC;

----- 3. Most contributing provider type----

SELECT provider_type, SUM(quantity) AS total_quantity
FROM food_listings
GROUP BY provider_type
ORDER BY total_quantity DESC;

------ 4. Most claimed food-----

SELECT f.food_name, COUNT(c.claim_id) AS total_claims
FROM claims c
JOIN food_listings f ON c.food_id = f.food_id
GROUP BY f.food_name
ORDER BY total_claims DESC;


----- 5. Total food quantity available ----

SELECT SUM(quantity) AS total_food_quantity
FROM food_listings;

------ 6. Top city by food listings -------

SELECT location, COUNT(*) AS total_food_listings
FROM food_listings
GROUP BY location
ORDER BY total_food_listings DESC;

------- 7. Most common food type------

SELECT food_type, COUNT(*) AS total_count
FROM food_listings
GROUP BY food_type
ORDER BY total_count DESC;

-------- 8. Claims per food item -------

SELECT f.food_name, COUNT(c.claim_id) AS total_claims
FROM food_listings f
LEFT JOIN claims c ON f.food_id = c.food_id
GROUP BY f.food_name
ORDER BY total_claims DESC;

------- 9. Provider with most successful claims------

SELECT p.name AS provider_name, COUNT(c.claim_id) AS successful_claims
FROM claims c
JOIN food_listings f ON c.food_id = f.food_id
JOIN providers p ON f.provider_id = p.provider_id
WHERE c.status = 'Completed'
GROUP BY p.name
ORDER BY successful_claims DESC;

-------- 10. Claim status percentage ------

SELECT status,
       COUNT(*) AS total_claims,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM claims
GROUP BY status
ORDER BY percentage DESC;


--------- 11. Average quantity claimed ------

SELECT ROUND(AVG(f.quantity), 2) AS average_quantity_claimed
FROM claims c
JOIN food_listings f ON c.food_id = f.food_id;

---------- -- 12. Most claimed meal type -------

SELECT f.meal_type, COUNT(c.claim_id) AS total_claims
FROM claims c
JOIN food_listings f ON c.food_id = f.food_id
GROUP BY f.meal_type
ORDER BY total_claims DESC;

----------- 13. Total donated quantity by provider----
SELECT p.name AS provider_name, SUM(f.quantity) AS total_donated_quantity
FROM providers p
JOIN food_listings f ON p.provider_id = f.provider_id
GROUP BY p.name
ORDER BY total_donated_quantity DESC;

----------- 14. Food nearing expiry ----------

SELECT food_name, quantity, expiry_date, location
FROM food_listings
WHERE expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '3 days'
ORDER BY expiry_date;

-------------- 15. City with highest completed claims -------

SELECT f.location, COUNT(c.claim_id) AS completed_claims
FROM claims c
JOIN food_listings f ON c.food_id = f.food_id
WHERE c.status = 'Completed'
GROUP BY f.location
ORDER BY completed_claims DESC;