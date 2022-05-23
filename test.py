import unittest

from wmsigner import Signer
import sys

# Для запуска тестов эти данные должны быть заполнены
signer = Signer(wmid='276752932432',
                keys='/home/ubuntu/wmkeys/276752932432.kwm',
                password='kickkick')


print('+++++',sys.getrecursionlimit(),'+++++')  # 1000
sys.setrecursionlimit(10000)
print('+++++',sys.getrecursionlimit(),'+++++')  # 1000

class TestWMSigner(unittest.TestCase):
    def test_equal(self):
        """
        Получение подписи без случайного добавления байт.
        """

        signature = 'a44bac57cf2efb356441e8c2b1bf6e79f414f99fe9cbd378f560ac' \
                    'ae49e9f96d7cc76e6b74a2caffad1c8c9d386f6b851944538169d5' \
                    'b381545302ff686f00af00a6'
        self.assertEqual(signer.sign('0000'), signature)

    def test_length(self):
        """
        Проверка длинны подписи.
        """

        for i in range(20):
            self.assertTrue(len(signer.sign(str(i))) == 132)

    def test_md4(self):
        """
        Проверка алгоритма MD4.
        """

        digest = b'\xf9\xfdW\xbfu\xcaU\xdb\xb4\x91}\x9f\x16\x9f\xcb\xbb'
        self.assertEqual(signer.md4('0000'), digest)
        print(signer.md4('0000'))

if __name__ == '__main__':
    unittest.main()