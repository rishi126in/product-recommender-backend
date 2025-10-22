from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.recommender import get_recommendations

@api_view(['POST'])
def recommend(request):
    query = request.data.get("query", "")
    if not query:
        return Response({"error": "Query is required"}, status=400)

    recommendations = get_recommendations(query)
    return Response({"products": recommendations})
