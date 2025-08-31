import unittest
from django.test.runner import DiscoverRunner

class ColorTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"✅ {test} PASSED")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"❌ {test} FAILED")

    def addError(self, test, err):
        super().addError(test, err)
        print(f"❌ {test} ERROR")

class ColorTestRunner(DiscoverRunner):
    def get_resultclass(self):
        return ColorTestResult
