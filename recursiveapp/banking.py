from django.db import models
from django.core.validators import RegexValidator

# ###### IBAN Field
# Write a Django custom Field model to store IBANs. The Field must meet the following requirements:
# 1. The stored value should never be fully visible - given an IBAN like "GR96 0810 0010 0000 0123 4567 890", 
#    the value should be displayed as "---7890" everywhere
# 2. Superusers should be able to see the full value when needed


# ------------------------------------------------------------------------------------------------------------------

ibanValidator = RegexValidator(r'[A-Z]{2}\d{2} ?\d{4} ?\d{4} ?\d{4} ?\d{4} ?[\d]{0,2}', "Enter a valid IBAN")
# For validation, I did choose a simple one. 

# Some accepted cases:
# FR23 1275 9945 4554 3422 
# GB84 2323 1232 2334 5767 2
# TR99 3373 3112 4528 3192 74

class ibanStorage(models.Model):
    name = models.CharField(max_length = 100)
    iban = models.CharField(validators=[ibanValidator])

    def __str__(self):
        return '---' + self.iban[-4:]

    def seeAll(self):
        return self.iban

# SUPERUSER or current user check can be handled on the view with authentication library:

# from django.contrib.auth import authenticate, login
# from app.models import ibanStorage

# if request.user.is_superuser:
#     return ibanStorage.seeAll()

# ------------------------------------------------------------------------------------------------------------------


# ###### Address deduplication
# Consider an Address model defined as follows:
#
# class UserAddress(models.Model):
#    user = models.ForeignKey(User)
#    name = models.CharField(max_length=255)
#    street_address = models.CharField(max_lenght=255)
#    street_address_line2 = models.CharField(max_lenght=255, blank=True, null=True)
#    zipcode = models.CharField(max_length=12, blank=True, null=True)
#    city = models.CharField(max_length=64)
#    state = models.CharField(max_length=64, blank=True, null=True)
#    country = models.CharField(max_length=2)
#    full_address = models.TextField(blank=True)
#    
#    def save(*args, **kwargs):
#        streetdata = f"{self.street_address}\n{self.street_address_line2}"
#        self.full_address = f"{streetdata}\n{self.zipcode} {self.city} {self.state} {self.country}"
#        super().save(*args, **kwargs)
#
# A UserAddress is saved every time the user changes something in the form, provided the form is valid.
# The task is devising a way of removing partial addresses that are entirely a subset of the current address.
# For example, assuming the following addresses are entered in the form(all belonging to the same user) in sequence:
#
# add1 = UserAddress(name="Max", city="Giventown")
# add2 = UserAddress(name="Max Mustermann", street_address="Randomstreet", city="Giventown")
# add3 = UserAddress(name="Max Mustermann", street_address="456 Randomstreet", city="Giventown")
# add4 = UserAddress(name="Max Mustermann", street_address="789 Otherstreet", city="Giventown", country="NL")
# 
# The expected result would be that only add3 and add4 are left in the DB at the end of the sequence


# ------------------------------------------------------------------------------------------------------------------

class UserAddress(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    street_address = models.CharField(max_lenght=255)
    street_address_line2 = models.CharField(max_lenght=255, blank=True, null=True)
    zipcode = models.CharField(max_length=12, blank=True, null=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=2)
    full_address = models.TextField(blank=True)

    def save(*args, **kwargs):
        streetdata = f"{self.street_address}\n{self.street_address_line2}"
        self.full_address = f"{streetdata}\n{self.zipcode} {self.city} {self.state} {self.country}"
        super().save(*args, **kwargs)

        repetitionCheck(self.name, self.street_address, self.street_address_line2, self.zipcode, self.city, self.state, self.country)
        # Calling the local repetitionCheck function with all of the address variables. 

    def repetitionCheck(new_name, new_street_address, new_street_address_line2, new_zipcode, new_city, new_state, new_country):
        new_items = [new_name, new_street_address, new_street_address_line2, new_zipcode, new_city, new_state, new_country]
        # Putting all of the new address variables to an array to generalize their check

        for row in UserAddress.objects.filter(user=user):
            # Getting recorded user addresses and looping through all of its rows

            notSame = False
            # This row is not unique at start, it has to prove itself
            
            for i in range(7):
                # New Address has 7 parameters in total, UserAddress has more but we don't need "user" and "full_address"

                if row[i+1] not in new_items[i]:
                    # First item of the row is "user", so we are passing that one

                    notSame = True
                    # If any row from before has a unique content, don't touch it

            if not notSame:
                row.delete()
                # If none of the columns of this row couldn't prove itself that it is unique, delete this row from the table.

# ------------------------------------------------------------------------------------------------------------------