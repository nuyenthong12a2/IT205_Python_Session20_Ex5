
from main import calc_actual_withdrawal

def run_tests():
    print("--- ĐANG CHẠY KIỂM THỬ RÚT VỐN ---")

  
    try:
        result1 = calc_actual_withdrawal(100)
        assert result1 == 90.0, f"Test 1 thất bại: Mong đợi 90.0, nhận được {result1}"
        print("Test Case 1 (Rút 100 nhận 90): OK")
    except Exception as e:
        print(f"Test Case 1 thất bại do lỗi: {e}")

   
    try:
        calc_actual_withdrawal(-10)
        print("Test Case 2 thất bại: Không phát hiện lỗi với số âm")
    except ValueError:
        print("Test Case 2 (Số âm sinh lỗi): OK")
    
    print("\n=> TẤT CẢ CÁC BÀI KIỂM THỬ ĐỀU THÀNH CÔNG!")

if __name__ == "__main__":
    run_tests()