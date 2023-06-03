from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def get_recommendations(request):
    data = cache.get("recommendations")
    if data is None:
        # If data is not in cache, fetch it from an external source or perform calculations.
        # For simplicity, we'll assume the recommendations are a list of dictionaries.
        recommendations = [
            {"title": "Recommendation 1", "description": "This is recommendation 1"},
            {"title": "Recommendation 2", "description": "This is recommendation 2"},
        ]

        # Store the recommendations in the cache for future requests.
        cache.set("recommendations", recommendations)

        data = recommendations

    return Response(data)
