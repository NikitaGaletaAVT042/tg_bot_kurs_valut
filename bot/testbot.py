import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram import types
from bot.bot import dp, send_rates, exchange_rate
import asyncio

class TestBotCommands(unittest.TestCase):

    def setUp(self):
        # Создаем mock Redis клиент
        self.redis_mock = MagicMock()
        self.redis_patch = patch('bot.bot.redis_client', self.redis_mock)
        self.redis_patch.start()

    def tearDown(self):
        self.redis_patch.stop()

    @patch('aiogram.Bot')
    def test_send_rates(self, mock_bot):
        # Настроим mock Redis для возвращения ожидаемых данных
        self.redis_mock.scan_iter.return_value = ['currency:USD', 'currency:RUB']
        self.redis_mock.get.side_effect = lambda key: {
            'currency:USD': '87.7805',
            'currency:RUB': '1.0'
        }.get(key)

        # Создаем mock сообщения
        mock_message = MagicMock()
        mock_message.answer = AsyncMock()

        # Вызовем команду /rates
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_rates(mock_message))

        # Проверка того, что message.answer был вызван с ожидаемым текстом
        mock_message.answer.assert_called_with('USD: 87.7805\nRUB: 1.0')

    @patch('aiogram.Bot')
    def test_exchange_rate(self, mock_bot):
        # Настроим mock Redis для возвращения ожидаемых данных
        self.redis_mock.get.side_effect = lambda key: {
            'currency:USD': '87.7805',
            'currency:RUB': '1.0'
        }.get(key)

        # Создаем mock сообщения
        mock_message = MagicMock()
        mock_message.text = '/exchange USD RUB 10'
        mock_message.answer = AsyncMock()

        # Вызовем команду /exchange
        loop = asyncio.get_event_loop()
        loop.run_until_complete(exchange_rate(mock_message))

        # Ожидаемый результат конвертации
        expected_amount = 10 * (87.7805 / 1.0)  # 10 USD в RUB
        expected_message = f'10 USD = {expected_amount:.2f} RUB'

        # Проверка того, что message.answer был вызван с ожидаемым текстом
        mock_message.answer.assert_called_with(expected_message)

if __name__ == '__main__':
    unittest.main()
