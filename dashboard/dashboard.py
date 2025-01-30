import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    data = pd.read_csv('https://drive.usercontent.google.com/u/0/uc?id=1D8i0FEUtSBaPvqfd9A77BsG8VxZZXE_7&export=download')
    return data

day = load_data()

st.title("Project Analisis Data : Bike Sharing")

st.markdown("""
            
- **Nama:** Muhammad Faqih
- **Email:** faqihtelco@gmail.com
- **ID Dicoding:** muhammad_faqih_kmwq
            
""")

st.header("Business Questions")
st.markdown("""
            
- Question 1 : Pada musim apa penyewaan sepeda paling ramai?
- Question 2 : Berapa total penyewaan sepeda pada bulan Maret 2012?
            
""")

st.subheader("")
st.subheader("Dataset will be used:")
st.write(day.head(15))
st.write("**Atribut Dataset**")

attributes = """

**Attributes:**
- **instant**: index
- **dteday**: bike rental date
- **season**: season (
- 1: Spring, 
- 2: Summer, 
- 3: Fall, 
- 4: Winter)
- **yr**: year (0: 2011, 1:2012)
- **mnth**: month (1 to 12)
- **hr**: hour (0 to 23)
- **holiday**: holiday
- **weekday**: day of the week
- **workingday**: weekday (1 if weekday, 0 if holiday)
- **weathersit**:
- 1: Sunny, Few clouds, Partly cloudy, Partly cloudy
- 2: Fog + Cloudy, Fog + Broken clouds, Fog + Few clouds, Fog
- 3: Light snow, Light rain + Thunderstorms + Scattered clouds, Light rain + Scattered clouds
- 4: Heavy rain + Ice + Thunderstorm + Fog, Snow + Fog
- **temp**: Temperature in Celsius
- **atemp**: Perceived temperature in Celsius.
- **hum**: Normalized humidity. The value is divided into 100 (max)
- **windspeed**: Normalized wind speed. The value is divided into 67 (max)
- **casual**: number of regular bike borrowers, who are not subscribed
- **registered**: number of bike borrowers who are registered members
- **cnt**: total number of bike borrowers (total bike borrowers both casual and registered)
"""

st.write(attributes)

def remove_outliers(df):
    df_numeric = df.select_dtypes(include=['number'])
    
    Q1 = df_numeric.quantile(0.25)
    Q3 = df_numeric.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    mask = (df_numeric >= lower_bound) & (df_numeric <= upper_bound)
    df_filtered = df_numeric[mask.all(axis=1)]
    
    return df[df.index.isin(df_filtered.index)]

day_cleaned = remove_outliers(day)

day['dteday'] = pd.to_datetime(day['dteday'])

st.subheader("Comparison of Bike Rental Trends 2011 & 2012")

def display_yearly_rental_trend(day):
    yearly_rental_trend = day.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='mnth', y='cnt', hue='yr', data=yearly_rental_trend, hue_order=[0, 1])
    plt.title('Bike Rental Trends per Month (2011 & 2012))')
    plt.xlabel('Months')
    plt.ylabel('Total Bike Rental')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend(title='Tahun', labels=['2011', '2012'])
    st.pyplot(plt)
    
display_yearly_rental_trend(day)

st.write("From the graph above, we can see that in 2011, from January to May, the number of bicycle rentals increased rapidly, but from October to the end of the year, there was a decline.  ")


day_2012 = day[day['yr'] == 1]

st.subheader("Monthly Bike Rental Trends in 2012")

monthly_rental_2012 = day_2012.groupby('mnth')['cnt'].sum()

fig2, ax2 = plt.subplots()
plt.plot(monthly_rental_2012.index, monthly_rental_2012.values, marker='o')
plt.title('Total Bike Rentals per Month in 2012')
plt.xlabel('Months')
plt.ylabel('Rental Total')
plt.xticks(monthly_rental_2012.index, ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.grid(True)
st.pyplot(fig2)

st.write("If we look further into 2012, a significant increase occurred in February-March, and the peak was in September. However, towards October, there was a sharp decline until the end of the year.")

total_rental_march_2012 = day_2012[day_2012['mnth'] == 3]['cnt'].sum()
st.write(f"Total bicycle rentals in March 2012: {total_rental_march_2012}")

st.subheader("Total Bike Rentals By Season")
season_counts = day.groupby('season')['cnt'].sum().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(x='season', y='cnt', data=season_counts, ax=ax1)
ax1.set_title('Total Bike Rentals By Season')
ax1.set_xlabel('Seasons')
ax1.set_ylabel('Rental Total')
ax1.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'], rotation=45)
st.pyplot(fig1)

st.write ("If we group the number of bicycle rentals based on the season, we can see that fall is the season with the highest number of bicycle rentals compared to other seasons.")

ramai_index = season_counts['season'][season_counts['cnt'].idxmax()]
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
ramai = season_mapping[ramai_index]

st.write(f"The season with the busiest bike loans: {ramai}")

st.header("Conclutions")

st.write("- Question 1 : Musim dengan penyewaan sepeda paling ramai adalah musim gugur (Fall)")

st.write(f"- Question 2 : Total penyewaan sepeda pada bulan Maret 2012: {total_rental_march_2012}")

