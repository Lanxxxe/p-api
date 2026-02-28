from rest_framework import serializers


class InternshipLogSerializer(serializers.Serializer):
    date = serializers.DateField()
    hours = serializers.FloatField()
    time_in = serializers.TimeField()
    time_out = serializers.TimeField()
    notes = serializers.CharField(max_length=500, allow_blank=True)


class ProjectSerializer(serializers.Serializer):
    project_name = serializers.CharField(max_length=200)
    summary = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    languages = serializers.CharField(required=True)
    project_url = serializers.URLField(required=True)
    project_image = serializers.CharField(required=False, allow_blank=True)
    category = serializers.JSONField(required=False)


class ToolSerializer(serializers.Serializer):
    tool_name = serializers.CharField(max_length=200)
    description = serializers.CharField(required=True)
    version = serializers.CharField(max_length=50, required=False, allow_blank=True)
    icon_url = serializers.CharField(required=False, allow_blank=True)
    category = serializers.JSONField(required=False)

class AchivementSerializer(serializers.Serializer):
    event = serializers.CharField(max_length=200)
    ranked = serializers.CharField(max_length=100)
    summary = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    location = serializers.CharField(max_length=200)
    date_achieved = serializers.DateField()
    proof_url = serializers.CharField(required=True)
    category = serializers.JSONField(required=False)

