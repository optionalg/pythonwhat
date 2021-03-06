import unittest
import helper

class TestMcRight(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '# pec comes here',
            "DC_CODE": 'selected_option = 2',
            "DC_SOLUTION": ''
        }

    def test_mcSuccess(self):
        self.data["DC_SCT"] = 'test_mc(2, ["This is wrong", "This is right"])'
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "This is right")


class TestMcWrong(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": '# pec comes here',
            "DC_CODE": 'selected_option = 3',
            "DC_SOLUTION": ''
        }

    def test_mcFail(self):
        self.data["DC_SCT"] = 'test_mc(2, ["This is wrong", "This is right", "Oh no, not correct"])'
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Oh no, not correct")

if __name__ == "__main__":
    unittest.main()