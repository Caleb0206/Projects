# Start of unittest - add to completely test functions in exp_eval

import unittest
from exp_eval import *

class test_expressions(unittest.TestCase):
    def test_helper_try_cast(self):
        try:
            helper_try_cast("abc")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Invalid token")
        self.assertEqual(helper_try_cast("12.3"), 12.3)
        self.assertEqual(helper_try_cast("1.0"), 1.0)
        self.assertEqual(helper_try_cast("12"), 12)

if __name__ == "__main__":
    unittest.main()
