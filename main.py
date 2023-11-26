import aiohttp
import sys
import asyncio
import platform
from datetime import datetime, timedelta


async def main(days, *currencies):
    async with aiohttp.ClientSession() as session:
        if int(days) <= 10:
            for i in range(int(days)):
                shift = (datetime.now() - timedelta(days=int(i))).strftime('%d.%m.%Y')
                try:
                    async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?date={shift}') as resp:
                        if resp.status == 200:
                            result = await resp.json()
                            formatted_data = []

                            for rate in result["exchangeRate"]:
                                if rate["currency"] in list(currencies) or rate["currency"] in ['EUR', 'USD']:
                                    date_key = shift
                                    currency_key = rate["currency"]
                                    sale_key = "sale"
                                    purchase_key = "purchase"

                                    formatted_entry = {date_key: {
                                        currency_key: {sale_key: rate["saleRateNB"], purchase_key: rate["purchaseRateNB"]}}}
                                    formatted_data.append(formatted_entry)
                            print(formatted_data)
                        else:
                            print(f"Error status: {resp.status}")
                except aiohttp.ClientConnectorError as err:
                    print(f'Connection error:', str(err))
        else:
            print('Maximum days = 10!')


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main(sys.argv[1], *sys.argv[2:]))