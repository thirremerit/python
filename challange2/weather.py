import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
data = pd.read_csv("weather_tokyo_data.csv")

# Remove extra spaces from column names
data.columns = data.columns.str.strip()

# Clean temperature column
data["temperature"] = data["temperature"].astype(str).str.strip()

# Remove parentheses
data["temperature"] = data["temperature"].str.replace("(", "", regex=False)
data["temperature"] = data["temperature"].str.replace(")", "", regex=False)

# Convert temperature to numbers
data["temperature"] = pd.to_numeric(data["temperature"], errors="coerce")

# Convert day column into dates
data["day"] = pd.to_datetime(data["day"], format="%m/%d")

# Extract month number
data["month"] = data["day"].dt.month

# Calculate yearly average
year_avg_temp = data["temperature"].mean()

print(f"Average temperature for the whole year: {year_avg_temp:.2f}°C")

# Monthly averages
monthly_avg_temp = data.groupby("month")["temperature"].mean()

print("\nAverage temperature for each month:")
print(monthly_avg_temp)

# Find hottest and coldest days
hottest_day = data.loc[data["temperature"].idxmax()]
coldest_day = data.loc[data["temperature"].idxmin()]

print("\nHottest Day:")
print(hottest_day[["day", "temperature"]])

print("\nColdest Day:")
print(coldest_day[["day", "temperature"]])

# Create line graph
plt.figure(figsize=(10, 5))

plt.plot(
    monthly_avg_temp.index,
    monthly_avg_temp.values,
    marker="o",
    label="Monthly Average Temperature"
)

# Add yearly average line
plt.axhline(
    year_avg_temp,
    linestyle="--",
    label=f"Year Avg: {year_avg_temp:.2f}°C"
)

# Plot hottest day
plt.scatter(
    hottest_day["month"],
    hottest_day["temperature"],
    s=100,
    label="Hottest Day"
)

# Plot coldest day
plt.scatter(
    coldest_day["month"],
    coldest_day["temperature"],
    s=100,
    label="Coldest Day"
)

# Labels for hottest and coldest points
plt.text(
    hottest_day["month"],
    hottest_day["temperature"],
    f'Hottest: {hottest_day["temperature"]}°C'
)

plt.text(
    coldest_day["month"],
    coldest_day["temperature"],
    f'Coldest: {coldest_day["temperature"]}°C'
)

# Labels and title
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.title("Tokyo Monthly Temperatures")

# Show legend
plt.legend()

# Show graph
plt.show()