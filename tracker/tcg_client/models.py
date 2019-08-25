from django.db import models
from django.core.validators import RegexValidator

price_regex = RegexValidator(r'^\d+\.\d{2}$', "This doesn't look like a price.")


class Card(models.Model):
    card_id = models.IntegerField(primary_key=True)
    card_name = models.CharField(max_length=100)
    img_url = models.URLField()
    tcg_player_link = models.URLField()
    card_effect = models.CharField(max_length=400)


class HistoricalPrice(models.Model):
    card_id = models.IntegerField()
    date_recorded = models.DateField(auto_now_add=True)
    market_price = models.CharField(validators=[price_regex], max_length=10)
    lowest_price = models.CharField(validators=[price_regex], max_length=10)
