import requests
import json

from config import money

class APIException(Exception):
    pass


class BankApi:

    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        try:
            base_key = money[base]
        except KeyError:
            raise APIException('Не удалось распознать первый параметр')

        try:
            quote_key = money[quote]
        except KeyError:
            raise APIException('Не удалось распознать второй параметр')

        if base_key == quote_key:
            raise APIException('Нет смыла в переводе одинаковых валют')

        try:
            amount_fl = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException('Не удалось распознать третий параметр')

        response = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={quote_key}')
        obj_response = json.loads(response.content)

        return amount_fl * obj_response[quote_key]
