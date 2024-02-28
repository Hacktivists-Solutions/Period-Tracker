from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class PeriodSymptom(models.Model):
    """
    Represents various symptoms associated with a menstrual cycle.

    Fields:
    - description: A text field describing the symptom.
    - symptom: An integer field with predefined choices (constants) for cramps, mood swings, and fatigue.

    Methods:
    - __str__(self): Returns a string representation of the symptom.

    Metaclass:
    - Specifies the plural name for this model (used in the admin interface).
    """

    CRAMPS = 1
    MOOD_SWINGS = 2
    FATIGUE = 3
    SYMPTOM_CHOICES = [
        (CRAMPS, _('Cramps')),
        (MOOD_SWINGS, _('Mood Swings')),
        (FATIGUE, _('Fatigue')),
    ]

    symptom = models.IntegerField(choices=SYMPTOM_CHOICES, db_index=True)

    def __str__(self):
        """Returns a human-readable string representation of the symptom."""
        return str(self.get_symptom_display())

    class Meta:
        verbose_name_plural = "Period Symptoms"

    def clean(self):
        """Performs additional model-level validation."""
        if self.symptom not in [choice[0] for choice in self.SYMPTOM_CHOICES]:
            raise ValidationError(_('Invalid symptom choice.'))


class MenstrualCycle(models.Model):
    """
    Represents a user's menstrual cycle.

    Fields: - user: A foreign key to the User model, indicating which user this menstrual cycle belongs to. -
    start_date: The date when the menstrual cycle begins. - end_date: The date when the menstrual cycle ends. -
    symptoms: A many-to-many relationship with the PeriodSymptom model, allowing multiple symptoms to be associated
    with a menstrual cycle. - notes: A text field for any additional notes related to the cycle.

    Methods:
    - __str__(self): Returns a human-readable string representation of the menstrual cycle.
    - duration(self): Calculates the duration of the cycle in days.
    - clean(self): Custom validation method to ensure that the end date is greater than the start date.

    Metaclass:
    - Specifies the plural name for this model (used in the admin interface).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    symptoms = models.ManyToManyField(
        'PeriodSymptom', related_name='periods', blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Menstrual cycle of {self.user.username} from {self.start_date} to {self.end_date}"

    def duration(self):
        """
        Calculates the duration of the menstrual cycle in days.
        """
        return (self.end_date - self.start_date).days + 1

    def clean(self):
        """
        Custom validation method to ensure that the end date is greater than the start date.
        Raises a ValidationError if the condition is not met.
        """
        if self.end_date < self.start_date:
            raise ValidationError(
                _("End date should be greater than start date."))

    class Meta:
        verbose_name_plural = "Menstrual Cycles"
