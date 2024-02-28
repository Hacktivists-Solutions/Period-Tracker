from django.contrib.auth.models import User
from rest_framework import serializers
from tracker.models import PeriodSymptom, MenstrualCycle


class PeriodSymptomSerializer(serializers.ModelSerializer):
    """
    Serializer for PeriodSymptom model.
    Includes the human-readable symptom name.
    """

    symptoms = serializers.CharField(source="get_symptom_display")

    class Meta:
        model = PeriodSymptom
        fields = ["symptoms", "id"]


class PeriodMenstrualCycle(serializers.ModelSerializer):
    """
    Serializer for MenstrualCycle model.
    Includes user information (username) and related symptoms.
    """

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    symptoms = PeriodSymptomSerializer(many=True, read_only=True)  # Set symptoms as read-only
    username = serializers.CharField(source="user.username")
    duration = serializers.SerializerMethodField(source="get_duration")

    @staticmethod
    def get_duration(obj):
        return f"{obj.duration()} days"

    def create(self, validated_data):
        # Create a new MenstrualCycle instance
        return MenstrualCycle.objects.create(user=self.context["request"].user, **validated_data)

    class Meta:
        model = MenstrualCycle
        fields = ["user", "username", "notes", "duration", "start_date", "end_date", "symptoms"]
