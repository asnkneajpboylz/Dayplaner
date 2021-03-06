import unittest
from Zeit import Zeit
from TimeManager import TimeManager as TM
from datetime import date
class TestZeit(unittest.TestCase):
    def test_Zeit_von_String(self):
        test1 = "13"
        test2 = "25"
        test3 = "14:30"
        test4 = "15:312"
        zeit1 = Zeit.fromString(test1)
        zeit2 = Zeit.fromString(test2)
        zeit3 = Zeit.fromString(test3)
        zeit4 = Zeit.fromString(test4)
        lsg1 = f"Zeit 13:00 am {zeit1.erhalteDatum()}"
        lsg3 = f"Zeit 14:30 am {zeit3.erhalteDatum()}"
        self.assertEqual(str(zeit1), lsg1)
        self.assertIsNone(zeit2, "Zeit richtig verworfen")
        self.assertEqual(str(zeit3), lsg3)
        self.assertIsNone(zeit4, "Zeit richtig verworfen")

    def test_circa(self):
        TM.genauigkeit = Zeit(0,5)
        zeit1 = Zeit(14, 35)
        zeit2 = Zeit(14, 32)
        zeit3 = Zeit(15, 00)
        self.assertTrue(zeit1.circa(zeit2))
        self.assertTrue(zeit2.circa(zeit2))
        self.assertFalse(zeit1.circa(zeit3))
        self.assertFalse(zeit3.circa(zeit1))

    def test_circa2(self):
        TM.genauigkeit = Zeit(0, 5)
        zeit1 = Zeit(14,35,date(2020,1,1))
        zeit2 = Zeit(14,35)
        zeit3 = Zeit(14,33, date(2020,1,1))
        self.assertFalse(zeit1.circa(zeit2))
        self.assertTrue(zeit1.circa(zeit3))
    def test_addition(self):
        zeit1 = Zeit(14, 35)
        zeit2 = Zeit(2, 0)
        zeit3 = Zeit(3, 30)
        zeit4 = Zeit(12, 30)
        self.assertEqual(str(zeit1 + zeit2), f"Zeit 16:35 am {zeit1.erhalteDatum()}")
        self.assertEqual(str(zeit1 + zeit3), f"Zeit 18:05 am {zeit1.erhalteDatum()}")
        # self.assertIsNone(str(zeit1 + zeit4))

    def test_subtraktion(self):
        zeit1 = Zeit(14, 35)
        zeit2 = Zeit(2, 0)
        zeit3 = Zeit(3, 40)
        zeit4 = Zeit(12, 30)
        self.assertEqual(str(zeit1 - zeit2), f"Zeit 12:35 am {zeit1.erhalteDatum()}")
        self.assertEqual(str(zeit1 - zeit3), f"Zeit 10:55 am {zeit1.erhalteDatum()}")
        # self.assertIsNone(str(zeit3 - zeit4))

    def test_groesser(self):
        zeit1 = Zeit(14, 35)
        zeit2 = Zeit(2, 0)
        zeit3 = Zeit(2, 0)
        zeit4 = Zeit(12, 30)

        self.assertTrue(zeit1 > zeit2)
        self.assertTrue(zeit1 > zeit4)
        self.assertFalse(zeit2 > zeit3)
        self.assertFalse(zeit4 > zeit1)

    def test_groesser2(self):
        zeit1 = Zeit(14, 35, date(2020,1,1))
        zeit2 = Zeit(2, 0, date(2020,1,2))
        self.assertTrue(zeit2 > zeit1)
    def test_groesser_gleich(self):
        zeit1 = Zeit(14, 35)
        zeit2 = Zeit(2, 0)
        zeit4 = Zeit(12, 30)

        self.assertTrue(zeit2 >= zeit2)
        self.assertFalse(zeit4 >= zeit1)
        self.assertTrue(zeit1 >= zeit2)

    def test_groesser_gleich2(self):
        zeit1 = Zeit(14, 35, date(2020, 1, 1))
        zeit2 = Zeit(2, 0, date(2020, 1, 2))
        self.assertTrue(zeit2 >= zeit1)
        self.assertTrue(zeit2 >= zeit2)

    def test_kleiner(self):
        zeit1 = Zeit(14, 35)
        zeit2 = Zeit(2, 0)
        zeit3 = Zeit(12, 30)

        self.assertTrue(zeit2 < zeit1)
        self.assertTrue(zeit3 < zeit1)
        self.assertFalse(zeit3 < zeit2)
        self.assertFalse(zeit2 < zeit2)

    def test_kleiner2(self):
        zeit1 = Zeit(14, 35, date(2020,1,1))
        zeit2 = Zeit(2, 0, date(2020,1,2))

        self.assertTrue(zeit1 < zeit2)
        self.assertFalse(zeit2 < zeit1)
    def test_runde(self):
        zeit1 = Zeit(14, 32)
        zeit2 = Zeit(2, 3)

        lsg1 = Zeit(14,30)
        lsg2 = Zeit(2,5)
        genauigkeit = Zeit(0,5)
        zeit1.runde(genauigkeit)
        zeit2.runde(genauigkeit)

        self.assertEqual(str(zeit1), str(lsg1))
        self.assertEqual(str(zeit2), str(lsg2))

if __name__ == '__main__':
    unittest.main()
