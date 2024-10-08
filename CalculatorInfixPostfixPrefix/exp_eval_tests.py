# Start of unittest - add to completely test functions in exp_eval

import unittest
from exp_eval import *
class test_expressions(unittest.TestCase):

    def test_postfix_eval_01(self):
        self.assertAlmostEqual(postfix_eval("3  5 +"), 8)
        self.assertAlmostEqual(postfix_eval("  5.2"), 5.2)


    def test_postfix_eval_02(self):
        try:
            postfix_eval("blah")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Invalid token")

        try:
            postfix_eval("2 ! +")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Invalid token")

    def test_postfix_eval_03_insufficient_operands(self):
        # test '+'
        try:
            postfix_eval(" 4 +")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        # test '-'
        try:
            postfix_eval("10 -")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        # test '*'
        try:
            postfix_eval("33 *")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        # test '/'
        try:
            postfix_eval("312 /")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        # test '**'
        try:
            postfix_eval("5 **")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")

        try:
            postfix_eval("  **")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")


    def test_postfix_eval_04_too_many_operands(self):
        try:
            postfix_eval("1 2 3 +")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Too many operands")

    # test an empty string
    def test_postfix_eval_05_empty(self):
        try:
            postfix_eval("")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Empty input")

    # test dividing by 0
    def test_postfix_eval_08_division(self):
        self.assertRaises(ValueError, postfix_eval, "1 0 /")
        self.assertAlmostEqual(postfix_eval("3 -2 /"), -1.5)
        self.assertAlmostEqual(postfix_eval("0 2 -"), -2)
    def test_postfix_eval_09_other(self):
        self.assertAlmostEqual(postfix_eval("6 4 3 + 2 - * 6 /"), 5)
        self.assertAlmostEqual(postfix_eval("5 1 2 + 4 ** + 3 -"), 83)
        self.assertAlmostEqual(postfix_eval("5 2 4 * + 7 2 - 4 6 2 / 2 - * + 4 - +"), 18)
    # test floats
    def test_postfix_eval_10_floats(self):
        self.assertAlmostEqual(postfix_eval("6.5 3.5 +"), 10.0)
        self.assertAlmostEqual(postfix_eval("6.5 2 * 3 -"), 10.0)

    # test shift operands
    def test_postfix_eval_11_shifts(self):
        try:
            postfix_eval("3 3 / 1 >>")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Illegal bit shift operand")

        try:
            postfix_eval("2.3 3 <<")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Illegal bit shift operand")

        try:
            postfix_eval("<< 5 3 +")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        # try an actual operation
        self.assertEqual(postfix_eval("8 1 >>"), 4)
        self.assertEqual(postfix_eval("2 1 <<"), 4)


    def test_infix_to_postfix_01(self):
        self.assertEqual(infix_to_postfix("6.0 - -5.0 ** 2"), "6.0 -5.0 2 ** -")
        self.assertEqual(infix_to_postfix("6 - 3"), "6 3 -")
        self.assertEqual(infix_to_postfix("6"), "6")
        self.assertEqual(infix_to_postfix("3 + 4 * 2 / ( 1 - 5 ) ** 2 ** 3"), "3 4 2 * 1 5 - 2 3 ** ** / +")
        self.assertEqual(infix_to_postfix("5 * ( 6 + 3 - 7 * 3 + 2 ) / 6"), "5 6 3 + 7 3 * - 2 + * 6 /")
        self.assertEqual(infix_to_postfix("8 + 3 * 4 + ( 6 - 2 + 2 * ( 6 / 3 - 1 ) - 3 )"),
                         "8 3 4 * + 6 2 - 2 6 3 / 1 - * + 3 - +")

        self.assertEqual(infix_to_postfix("8 >> 3 + 2"),"8 3 >> 2 +")
        self.assertEqual(infix_to_postfix("4 << 2 ** 4"), "4 2 << 4 **")
        self.assertEqual(infix_to_postfix("0 - 3"), "0 3 -")

        self.assertEqual(infix_to_postfix("2 + 3 * 4"), "2 3 4 * +")
        self.assertEqual(infix_to_postfix("( 2 + 3 ) * 4"), "2 3 + 4 *")
        self.assertEqual(infix_to_postfix("2 - ( 3 + 4 )"), "2 3 4 + -")
        self.assertEqual(infix_to_postfix("10 ** 3 + 4"), "10 3 ** 4 +")
        self.assertEqual(infix_to_postfix("10 * 3 ** 4"), "10 3 4 ** *")
        self.assertEqual(infix_to_postfix("( 10 ** 3 ) * ( 4 + 1 )"), "10 3 ** 4 1 + *")
        self.assertEqual(infix_to_postfix("3 * 10 ** 3  * 4 + 1"), "3 10 3 ** * 4 * 1 +")
        self.assertEqual(infix_to_postfix("( 15 / 3 ) << 2"), "15 3 / 2 <<")
        self.assertEqual(infix_to_postfix("16 << 3 + 4"), "16 3 << 4 +")

    def test_prefix_to_postfix(self):
        self.assertEqual(prefix_to_postfix("* - 3 / 2 1 - / 4 5 6"), "3 2 1 / - 4 5 / 6 - *")
        self.assertEqual(prefix_to_postfix("+ 2 -1"), "2 -1 +")
        self.assertEqual(prefix_to_postfix("1.3"), "1.3")
        self.assertEqual(prefix_to_postfix("+ << 2 3 4"), "2 3 << 4 +")
        self.assertEqual(prefix_to_postfix("+ 3.3 * 4 -5.2"), "3.3 4 -5.2 * +")
        self.assertEqual(prefix_to_postfix("+ * 5 4 - 6 2"), "5 4 * 6 2 - +")
        self.assertEqual(prefix_to_postfix("+ * 4 3 / 6 2"), "4 3 * 6 2 / +")
        self.assertEqual(prefix_to_postfix("** 5 2"), "5 2 **")
        self.assertEqual(prefix_to_postfix("+ ** 3 2 * 4 2"),"3 2 ** 4 2 * +")
    def test_grader_fails(self):
        self.assertAlmostEqual(12.0, postfix_eval("12"))
        self.assertAlmostEqual(9.0, postfix_eval("12 3 -"))
        self.assertAlmostEqual(23.1, postfix_eval("5 7.1 + 11 +"))
        self.assertAlmostEqual(-13.1, postfix_eval("5 7.1 - 11 -"))
        self.assertAlmostEqual(0.625, postfix_eval("2 1.25 * 0.25 *"))
        self.assertAlmostEqual(3.25, postfix_eval("13 2 / 2.0 /"))
        self.assertAlmostEqual(8.0, postfix_eval("4 0.5 ** 3 **"))



    def test_negative(self):
        self.assertAlmostEqual(-3, postfix_eval("-4 1 +"))
        self.assertAlmostEqual(512, postfix_eval("2 3 2 ** **"))
if __name__ == "__main__":
    unittest.main()
