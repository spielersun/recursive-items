from django.db import models
from django.core.validators import RegexValidator

acceptable_chars = RegexValidator(r'[A-Za-z0-9_]+', "Function name should only contain letters and numbers. ")

class recursiveFunctions(models.Model):
    name = models.CharField(max_length = 50, default = "name", unique=True, validators=[acceptable_chars])
    field_one = models.CharField(max_length = 50)
    field_two = models.CharField(max_length = 50)
    math_function = models.ForeignKey('mathFunctions', default = 1, on_delete=models.DO_NOTHING)
    objects = models.Manager()

    def __str__(self):
        return self.name

class mathFunctions(models.Model):
    function_name = models.CharField(max_length = 50)
    objects = models.Manager()

    def __str__(self):
        return self.function_name
        
    def __unicode__(self):
        return self.function_name