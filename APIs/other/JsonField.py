import json

from django.db import models
from django.core.exceptions import ValidationError
from django import forms
from rest_framework import serializers
import re


class SerializerJsonField(serializers.Field):
    def to_representation(self, obj):
        try:
            return json.loads(obj.replace("'", '"'))
        except:
            return obj

    def to_internal_value(self, data):
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            raise serializers.ValidationError("Invalid JSON format")
        return json_data


class JsonField(models.TextField):

    def validate_json(self, value):
        pass

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return value

    def to_db_value(self, value, expression, connection):
        if value is None:
            return None
        self.validate_json(value)
        return json.dumps(value)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        self.validate_json(value)
        return value

    def formfield(self, **kwargs):
        defaults = {'widget': forms.Textarea}
        defaults.update(kwargs)
        return super().formfield(**defaults)


"""
[
{
"lat": 28.7041,
"lng": 77.1025
}

]

"""
