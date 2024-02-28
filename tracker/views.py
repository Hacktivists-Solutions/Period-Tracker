# views.py
import json
from datetime import datetime

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MenstrualCycle, PeriodSymptom
from .serializers import PeriodMenstrualCycle, PeriodSymptomSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_menstrual_cycle(request):
    """
    API endpoint to record a new menstrual cycle.
    Input: JSON data containing cycle details.
    Output: Serialized cycle data or error messages.
    """

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    start_date = data.get("start_date")
    end_date = data.get("end_date")
    symptoms = data.get("symptoms")

    if not start_date or not end_date or not symptoms:
        return JsonResponse({'error': 'Missing required data'}, status=400)

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    body = {
        "user": request.user,
        "start_date": start_date,
        "end_date": end_date,
    }
    menstrual_cycle = MenstrualCycle.objects.create(**body)
    for symptom_data in symptoms:
        serializer = PeriodSymptomSerializer(data={"symptoms": symptom_data})
        if serializer.is_valid():
            symptom_instance, created = PeriodSymptom.objects.get_or_create(
                symptom=serializer.data["symptoms"])
            menstrual_cycle.symptoms.add(symptom_instance)
        else:
            print(f"Symptom serializer errors: {serializer.errors}")
    serializer = PeriodMenstrualCycle(instance=menstrual_cycle)

    return JsonResponse(serializer.data, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_menstrual_cycles(request):
    """
    API endpoint to retrieve all menstrual cycles for the authenticated user.
    Output: List of serialized cycle data.
    """
    try:
        cycles = MenstrualCycle.objects.filter(user=request.user)
        serializer = PeriodMenstrualCycle(cycles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_menstrual_cycles(request):
    """
    API endpoint to filter menstrual cycles by date range.
    Example usage: /api/cycles/?start_date=2024-01-01&end_date=2024-02-29
    Input: Query parameters start_date and end_date (ISO date format).
    Output: List of serialized cycle data within the specified range.
    """

    start_date_str = request.query_params.get('start_date')
    end_date_str = request.query_params.get('end_date')

    # converting dates into datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    if start_date > end_date:
        return Response({"error": "Start date is more than end date"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cycles = MenstrualCycle.objects.filter(user=request.user,
                                               start_date__gte=start_date,
                                               end_date__lte=end_date)
        serializer = PeriodMenstrualCycle(cycles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)


