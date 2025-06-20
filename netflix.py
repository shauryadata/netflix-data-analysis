import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Netflix Content Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("netflix1.xlsx")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    return df.dropna(subset=['year_added'])

df = load_data()

# Sidebar filters
st.sidebar.title("🔍 Filter Content")
selected_type = st.sidebar.multiselect("Select Content Type", options=df['type'].unique(), default=list(df['type'].unique()))
min_year, max_year = int(df['year_added'].min()), int(df['year_added'].max())
selected_years = st.sidebar.slider("Select Year Range", min_value=min_year, max_value=max_year, value=(2015, max_year))
selected_country = st.sidebar.multiselect("Select Country", options=df['country'].dropna().unique(), default=[])

# Filter data
filtered_df = df[
    (df['type'].isin(selected_type)) &
    (df['year_added'].between(selected_years[0], selected_years[1]))
]

if selected_country:
    filtered_df = filtered_df[filtered_df['country'].isin(selected_country)]

# Title
st.title("📊 Netflix Content Analytics Dashboard")
st.markdown(f"**{len(filtered_df)} records** between {selected_years[0]} and {selected_years[1]}")

# 1. Content type distribution
st.subheader("🎬 Content Type Distribution")
type_counts = filtered_df['type'].value_counts()
fig1, ax1 = plt.subplots()
sns.barplot(x=type_counts.index, y=type_counts.values, ax=ax1)
ax1.set_ylabel("Number of Titles")
st.pyplot(fig1)

# 2. Year-wise content additions
st.subheader("📅 Content Added Over Time")
yearly_add = filtered_df['year_added'].value_counts().sort_index()
fig2, ax2 = plt.subplots()
sns.lineplot(x=yearly_add.index, y=yearly_add.values, marker='o', ax=ax2)
ax2.set_xlabel("Year")
ax2.set_ylabel("Titles Added")
st.pyplot(fig2)

# 3. Top contributing countries
st.subheader("🌍 Top Countries by Content")
top_countries = filtered_df['country'].value_counts().head(10)
fig3, ax3 = plt.subplots()
sns.barplot(y=top_countries.index, x=top_countries.values, ax=ax3)
ax3.set_xlabel("Number of Titles")
st.pyplot(fig3)

# 4. Rating distribution
st.subheader("🔞 Content Rating Distribution")
rating_counts = filtered_df['rating'].value_counts().head(10)
fig4, ax4 = plt.subplots()
sns.barplot(x=rating_counts.index, y=rating_counts.values, ax=ax4)
ax4.set_ylabel("Number of Titles")
st.pyplot(fig4)

# 5. Most common genres
st.subheader("📚 Common Genres")
genre_expanded = filtered_df['listed_in'].dropna().str.split(', ').explode()
top_genres = genre_expanded.value_counts().head(10)
fig5, ax5 = plt.subplots()
sns.barplot(y=top_genres.index, x=top_genres.values, ax=ax5)
ax5.set_xlabel("Count")
st.pyplot(fig5)
