import unittest

def calc_actual_withdrawal(withdraw_amount: float) -> float:
    """
    Hàm tính số token thực nhận sau khi trừ 10% phí giao dịch.
    Công thức: Số thực nhận = Số rút - (Số rút * 0.1)
    """
    if withdraw_amount < 0:
        raise ValueError("Số token rút không được là số âm")
    return float(withdraw_amount * 0.9)

class TestFantasySystem(unittest.TestCase):
    
    def test_withdrawal_valid(self):
        """Test Case 1: Nhập 100 ➔ Trả về 90.0"""
        self.assertEqual(calc_actual_withdrawal(100), 90.0)

    def test_withdrawal_negative(self):
        """Test Case 2: Nhập số âm ➔ Sinh ra lỗi ValueError"""
        with self.assertRaises(ValueError):
            calc_actual_withdrawal(-50)

    def test_withdrawal_zero(self):
        """Test Case 3: Nhập 0 ➔ Trả về 0.0"""
        self.assertEqual(calc_actual_withdrawal(0), 0.0)

if __name__ == '__main__':
    unittest.main()