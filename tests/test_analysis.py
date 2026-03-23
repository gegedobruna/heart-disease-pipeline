import unittest
from pipeline.analysis import mean, median, std_dev, value_distribution, disease_rate_by_group


class TestMean(unittest.TestCase):

    def test_mean_simple(self):
        self.assertEqual(mean([1, 2, 3, 4, 5]), 3.0)

    def test_mean_with_nones(self):
        self.assertEqual(mean([1, None, 3, None, 5]), 3.0)

    def test_mean_empty_list(self):
        self.assertIsNone(mean([]))


class TestMedian(unittest.TestCase):

    def test_median_odd_length(self):
        self.assertEqual(median([1, 2, 3, 4, 5]), 3)

    def test_median_even_length(self):
        self.assertEqual(median([1, 2, 3, 4]), 2.5)


class TestStdDev(unittest.TestCase):

    def test_std_dev_known_value(self):
        # std dev of [2, 4, 4, 4, 5, 5, 7, 9] is exactly 2.0
        result = std_dev([2, 4, 4, 4, 5, 5, 7, 9])
        self.assertAlmostEqual(result, 2.0)


class TestDiseaseRateByGroup(unittest.TestCase):

    def test_disease_rate_by_group(self):
        records = [
            {"Sex": "1", "Heart Disease": "Presence"},
            {"Sex": "1", "Heart Disease": "Absence"},
            {"Sex": "0", "Heart Disease": "Presence"},
            {"Sex": "0", "Heart Disease": "Presence"},
        ]
        result = disease_rate_by_group(records, "Sex")
        self.assertEqual(result["1"]["rate"], 50.0)
        self.assertEqual(result["0"]["rate"], 100.0)


if __name__ == "__main__":
    unittest.main()