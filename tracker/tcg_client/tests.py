from contextlib import contextmanager

from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import HistoricalPrice

class ValidationErrorTestMixin(object):

    @contextmanager
    def assertValidationErrors(self, fields):
        """
        Assert that a validation error is raised, containing all the specified
        fields, and only the specified fields.
        """
        try:
            yield
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertEqual(set(fields), set(e.message_dict.keys()))


# Create your tests here.
class HistoricalPriceTestCases(ValidationErrorTestMixin, TestCase):
    def setUp(self):
        HistoricalPrice.objects.create(card_id=1, market_price="00.00", lowest_price="00.00")

    def test_price_regex(self):
        test_point = HistoricalPrice.objects.get(card_id=1)
        bad_prices = ['barf', "00000", "123.456", "-123", "10.9", "a110.30"]
        for bad_price in bad_prices:
            test_point.market_price = bad_price
            #TODO I don't know how to show the failing test case inside the error message
            with self.assertValidationErrors(['market_price']):
                test_point.full_clean()
            print(f"{bad_price} successfully raised a ValidationError")