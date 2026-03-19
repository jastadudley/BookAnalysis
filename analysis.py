import pandas as pd
import matplotlib.pyplot as plt

#BookAnalysis - GoodReads Dataset Analysis
#Author: Jasta Dudley
#Discription: Analyzes book data to answer two questions: 
#1. Does the book legnth correlate with average rating?
#2. Which popular books have the most polerized ratings?

# Load the dataset from Kaggle GoodReads CSV:
df = pd.read_csv('books.csv', on_bad_lines='skip')

# This section is cleaning the data:
df['num_pages'] = pd.to_numeric(df['  num_pages'], errors='coerce')
df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce')
df['ratings_count'] = pd.to_numeric(df['ratings_count'], errors='coerce')
# Dropping roaws where data is missing essentual numbers:
df = df.dropna(subset=['num_pages', 'average_rating', 'ratings_count'])
# Removing books with 0 pages/ bad data that would mess up the code.
df = df[df['num_pages'] > 0]

# Dataset Summery- prints general stats about the book/ dataset before analysis
print("===============================================================")
print("DATASET SUMMERY")
print("===============================================================")
total_books = len(df)
avg_pages = round (df['num_pages'].mean(), 1)
avg_rating = round(df['average_rating'].mean(), 2)
max_pages = int(df['num_pages'].max())
min_pages = int(df['num_pages'].min())
most_rated = df.loc[df['ratings_count'].idxmax(), 'title']

print(f"Total books in dataset: {total_books}")
print(f"Average page count: {avg_pages}")
print(f"Average rating across all books: {avg_rating}")
print(f"Longest book: {max_pages}")
print(f"Shortest book: {min_pages}")
print(f"Most rated book: {most_rated}")

# Store these key stats in a list for reference later
summary_stats = [total_books, avg_pages, avg_rating, max_pages, min_pages]
print(f"\nSummary stats list: {summary_stats}")

# --- QUESTION 1: Does book length correlate with average rating? ---
print("\n============================================================")
print("QUESTION 1: Book Length vs Average Rating")
print("============================================================")

# Define page count buckets to group books by length
bins = [0, 100, 200, 300, 400, 500, 750, 1000, 5000]
labels = ['<100', '100-200', '200-300', '300-400', '400-500', '500-750', '750-1000', '1000+']

# Create a new column assigning each book to a length category
df['length_category'] = pd.cut(df['num_pages'], bins=bins, labels=labels)

# Calculate average rating for each length category
avg_rating_by_length = df.groupby('length_category', observed=True)['average_rating'].mean()
print(avg_rating_by_length)

# Count how many books fall in each category
book_counts = df.groupby('length_category', observed=True)['title'].count()
print("\nBooks per category:")
print(book_counts)

# Plot bar chart of average rating by page count category
plt.figure(figsize=(10, 5))
avg_rating_by_length.plot(kind='bar', color='steelblue', edgecolor='black')
plt.title('Average Book Rating by Page Count Category')
plt.xlabel('Number of Pages')
plt.ylabel('Average Rating')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('graph1_length_vs_rating.png')
plt.show()

# ---- QUESTION 2: Most polarized popular books ----
print("\n============================================================")
print("QUESTION 2: Most Polarizing Popular Books")
print("============================================================")

# Filter to only books with significant readership (10,000+ ratings)
popular_books = df[df['ratings_count'] > 10000].copy()

# Calculate how far each book's rating deviates from the average
mean_rating = popular_books['average_rating'].mean()
popular_books['rating_deviation'] = abs(popular_books['average_rating'] - mean_rating)

# Get the top 10 most polarizing books
top_polarizing = popular_books.nlargest(10, 'rating_deviation')[['title', 'average_rating', 'ratings_count']]
print(top_polarizing)

# Check if any polarizing books are above or below average
above_avg = top_polarizing[top_polarizing['average_rating'] > mean_rating]
below_avg = top_polarizing[top_polarizing['average_rating'] < mean_rating]
print(f"\nPolarizing books ABOVE average: {len(above_avg)}")
print(f"Polarizing books BELOW average: {len(below_avg)}")

# Plot horizontal bar chart of most polarizing books
plt.figure(figsize=(12, 6))
plt.barh(top_polarizing['title'].str[:40], top_polarizing['average_rating'], color='tomato', edgecolor='black')
plt.axvline(mean_rating, color='navy', linestyle='--', label='Average Rating')
plt.title('Most Polarizing Popular Books (Furthest from Average Rating)')
plt.xlabel('Average Rating')
plt.legend()
plt.tight_layout()
plt.savefig('graph2_polarizing_books.png')
plt.show()

print("\nDone! Both graphs saved.")