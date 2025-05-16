from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def update(self, instance, validated_data):
        # Allow only these fields to be updated
        allowed_fields = ['status', 'worked_hours', 'completion_report']

        for field in validated_data:
            if field not in allowed_fields:
                raise serializers.ValidationError(
                    f"Updating '{field}' is not allowed."
                )

        # Additional rule: if marking completed, require both fields
        if validated_data.get('status') == 'COMPLETED' and instance.status != 'COMPLETED':
            if not validated_data.get('worked_hours'):
                raise serializers.ValidationError({"worked_hours": "This field is required when completing a task."})
            if not validated_data.get('completion_report'):
                raise serializers.ValidationError({"completion_report": "This field is required when completing a task."})

        return super().update(instance, validated_data)
