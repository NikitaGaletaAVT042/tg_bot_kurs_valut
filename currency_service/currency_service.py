import aiohttp
import asyncio
import redis
import xml.etree.ElementTree as ET

REDIS_HOST = 'redis'
REDIS_PORT = 6379
XML_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def fetch_currency_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(XML_URL) as response:
            xml_content = await response.text()
            return xml_content

def parse_and_store(xml_content):
    root = ET.fromstring(xml_content)
    for child in root.findall('Valute'):
        char_code = child.find('CharCode').text
        value = float(child.find('Value').text.replace(',', '.'))
        redis_client.set(f'currency:{char_code}', value)

async def update_currency_data():
    xml_content = await fetch_currency_data()
    parse_and_store(xml_content)

def main():
    asyncio.run(update_currency_data())

if __name__ == '__main__':
    main()
