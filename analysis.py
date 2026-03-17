import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('books.csv', on_bad_lines='skip')

# Clean the data
df['num_pages'] = pd.to_numeric(df['  num_pages'], errors='coerce')
df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce')
df['ratings_count'] = pd.to_numeric(df['ratings_count'], errors='coerce')
df = df.dropna(subset=['num_pages', 'average_rating', 'ratings_count'])
df = df[df['num_pages'] > 0]

# --- QUESTION 1: Does book length correlate with average rating? ---
print("=== Question 1: Book Length vs Average Rating ===")

# Group books into length categories
bins = [0, 100, 200, 300, 400, 500, 750, 1000, 5000]
labels = ['<100', '100-200', '200-300', '300-400', '400-500', '500-750', '750-1000', '1000+']
df['length_category'] = pd.cut(df['num_pages'], bins=bins, labels=labels)

avg_rating_by_length = df.groupby('length_category', observed=True)['average_rating'].mean()
print(avg_rating_by_length)

plt.figure(figsize=(10, 5))
avg_rating_by_length.plot(kind='bar', color='steelblue', edgecolor='black')
plt.title('Average Book Rating by Page Count Category')
plt.xlabel('Number of Pages')
plt.ylabel('Average Rating')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('graph1_length_vs_rating.png')
plt.show()

# --- QUESTION 2: Which books have the most polarized ratings? ---
print("\n=== Question 2: Most Polarized Books by Ratings Count Spread ===")

# Use ratings_count as popularity proxy, find extremes in rating among popular books
popular_books = df[df['ratings_count'] > 10000].copy()
popular_books['rating_deviation'] = abs(popular_books['average_rating'] - popular_books['average_rating'].mean())

top_polarizing = popular_books.nlargest(10, 'rating_deviation')[['title', 'average_rating', 'ratings_count']]
print(top_polarizing)

plt.figure(figsize=(12, 6))
plt.barh(top_polarizing['title'].str[:40], top_polarizing['average_rating'], color='tomato', edgecolor='black')
plt.axvline(popular_books['average_rating'].mean(), color='navy', linestyle='--', label='Average Rating')
plt.title('Most Polarizing Popular Books (Furthest from Average Rating)')
plt.xlabel('Average Rating')
plt.legend()
plt.tight_layout()
plt.savefig('graph2_polarizing_books.png')
plt.show()

print("\nDone! Both graphs saved.")