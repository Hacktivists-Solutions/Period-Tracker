from datetime import datetime, timedelta

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from analytics.util import avg_cycle
from tracker.models import MenstrualCycle
from tracker.serializers import PeriodMenstrualCycle


# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def avg_cycle_length(request):
    """
    Calculates the average length of menstrual cycles for the authenticated user.

    Returns:
        Response: A JSON response containing the average cycle length (in days).
                  If no cycles are found, returns an average of 0.
                  If an error occurs, provides an error message.
    """
    try:
        # Retrieve menstrual cycles associated with the authenticated user
        menstrual_cycles = MenstrualCycle.objects.filter(user=request.user)

        response = avg_cycle(menstrual_cycles)
        return Response(data={"avg_cycle": response})

    except MenstrualCycle.DoesNotExist:
        return Response(data={"error": "No menstrual cycles found for this user."})

    except ValueError:
        return Response(data={"error": "Invalid date format or calculation error."})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def avg_cycle_over_period(request):
    """
    Calculates the average menstrual cycle length over a specified period of time.
    Example usage: /api/cycles/?start_date=2024-01-01&end_date=2024-02-29
    Input: Query parameters start_date and end_date (ISO date format).
    Output: Avg cycle of periods within the specified range.

    Args:
        request: Django request object containing user information.

    Returns:
        JsonResponse: A JSON response containing the average cycle length (in days)
                      for the user's menstrual cycles within the specified period.
                      If no cycles are found, returns an average of 0.
                      If an error occurs, provides an error message.
    """
    try:
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        if start_date_str is None or end_date_str is None:
            return Response(data={"error": "Return a valid Start/End Date"}, status=400)

        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        # Retrieve menstrual cycles within the specified period
        menstrual_cycles = MenstrualCycle.objects.filter(
            user=request.user,
            start_date__gte=start_date,
            end_date__lte=end_date
        )

        if not menstrual_cycles.exists():
            return JsonResponse({"error": "No menstrual cycles found for the user within the specified period."},
                                status=404)

        # Calculate average cycle length
        average_cycle_length = avg_cycle(menstrual_cycles)

        if average_cycle_length is None:
            return JsonResponse({"error": "Average cycle length could not be calculated."}, status=404)

        return JsonResponse({"avg_cycle": average_cycle_length})

    except ValueError:
        return JsonResponse({"error": "Invalid date format. Please use ISO format (YYYY-MM-DD)."}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def predict_future_periods_view(request):
    """
    Predicts the next period date for a user based on their menstrual cycle data.

    Args:
        request: Django request object containing user information.

    Returns:
        JsonResponse: A JSON response with the predicted next period date or an error message.
    """

    menstrual_cycles = MenstrualCycle.objects.filter(user=request.user)
    if not menstrual_cycles.exists():
        return JsonResponse({'error': 'No menstrual cycles found for the user'}, status=404)

    average_cycle_length = avg_cycle(menstrual_cycles)
    if average_cycle_length is None:
        return JsonResponse({'error': 'Average cycle length could not be calculated'}, status=500)

    latest_cycle = menstrual_cycles.order_by('-end_date').first()
    next_period_date = latest_cycle.end_date + \
        timedelta(days=average_cycle_length)

    return JsonResponse({'next_period_date': next_period_date.strftime('%Y-%m-%d')})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def identify_symptom_patterns(request):
    """
    Identifies symptom patterns based on the user's menstrual cycle data.

    Args:
        request: Django request object containing user information.

    Returns:
        JsonResponse: A JSON response containing symptom patterns and occurrences.
                      If no cycles are found, returns an empty list.
    """
    cycles = MenstrualCycle.objects.filter(user=request.user)
    serializer = PeriodMenstrualCycle(cycles, many=True)

    symptom_patterns = {}  # Initialize an empty dictionary

    for cycle in serializer.data:
        symptoms = cycle['symptoms']
        for symptom in symptoms:
            if symptom['id'] not in symptom_patterns:
                symptom_patterns[symptom['id']] = {
                    "name": symptom['symptoms'],
                    "occurrences": 1
                }
            else:
                symptom_patterns[symptom['id']]["occurrences"] += 1

    return JsonResponse({'symptom_patterns': list(symptom_patterns.values())})
