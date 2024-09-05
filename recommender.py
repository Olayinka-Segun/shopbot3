from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.sql import func
from auth.models import User, SearchHistory, Product

# Collaborative Filtering
def collaborative_filtering(user_id):
    # Find users with similar search history
    similar_users = User.query.join(SearchHistory).filter(SearchHistory.user_id != user_id).all()

    # Collect products that similar users have interacted with
    recommended_products = []
    for user in similar_users:
        user_searches = SearchHistory.query.filter_by(user_id=user.id).all()
        for search in user_searches:
            products = Product.query.filter(Product.id.in_(search.results)).all()
            recommended_products.extend(products)

    # Return top recommendations, filtering duplicates
    unique_products = list({product.id: product for product in recommended_products}.values())
    return unique_products[:5]  # Return top 5 recommendations

# Content-Based Filtering
def content_based_filtering(user_id):
    # Get user's search history
    user_history = SearchHistory.query.filter_by(user_id=user_id).all()
    queries = [history.query for history in user_history]

    # TF-IDF vectorization of the product titles and user queries
    vectorizer = TfidfVectorizer()
    all_titles = [product.title for product in Product.query.all()]
    vectors = vectorizer.fit_transform(queries + all_titles)

    # Calculate cosine similarity between user queries and product titles
    user_vector = vectors[:len(queries)]
    product_vectors = vectors[len(queries):]
    similarity_scores = cosine_similarity(user_vector, product_vectors)

    # Find top products based on similarity scores
    top_indices = similarity_scores.argsort().flatten()[-5:]  # Top 5 products
    top_products = [Product.query.get(i + 1) for i in top_indices]

    return top_products

# Helper function to format recommendations
def format_recommendations(recommendations):
    formatted_results = "Top Recommendations:\n"
    for product in recommendations:
        formatted_results += f"Product: {product.title}\nPrice: {product.price}\nRating: {product.rating}\nLink: {product.link}\n\n"
    return formatted_results
