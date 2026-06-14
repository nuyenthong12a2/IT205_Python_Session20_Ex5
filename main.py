import logging
from typing import List, Dict

logging.basicConfig(
    filename="fantasy_league.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

players = [
    {"player_id": "T101", "name": "Faker", "market_value": 5000, "fan_tokens": 1500, "match_points": 0, "form_multiplier": 1.0},
    {"player_id": "GEN01", "name": "Chovy", "market_value": 4800, "fan_tokens": 800, "match_points": 500, "form_multiplier": 1.2},
    {"player_id": "DRX01", "name": "Deft", "market_value": 3000, "fan_tokens": 0, "match_points": 0, "form_multiplier": 0.8},
]

def find_player_by_id(players: List[Dict], player_id: str) -> int:
    for i, p in enumerate(players):
        if p.get("player_id", "").upper() == player_id.upper():
            return i
    return -1  # Phải đưa ra ngoài vòng lặp!

def display_market(players: List[Dict]) -> None:
    print("\n--- SÀN GIAO DỊCH TUYỂN THỦ ---")
    if not players:
        print("Sàn giao dịch hiện chưa có tuyển thủ nào.")
        return 
    print(f"{'ID':<8}|{'Tên':<10}|{'Giá':<10}|{'Token':<8}|{'Điểm':<8}|{'Hệ số':<6}|{'Trạng thái'}")
    print("-" * 80)
    for p in players:
        tokens = p.get("fan_tokens", 0)
        status = "Tuyển thủ Hot" if tokens > 1000 else "Đang thu hút" if tokens > 0 else "Chưa có người đầu tư"
        print(f"{p.get('player_id'):<8}|{p.get('name'):<10}|{p.get('market_value'):<10}|{tokens:<8}|{p.get('match_points'):<8}|{p.get('form_multiplier'):<6}|{status}")
    logging.info("User viewed the player market")

def invest_tokens(players: List[Dict]) -> None:
    pid = input("Nhập mã tuyển thủ: ")
    idx = find_player_by_id(players, pid)
    if idx == -1:
        print("Không tìm thấy tuyển thủ!")
        logging.warning(f"Invest failed - Player {pid} not found")
        return 
    
    try:
        amount = int(input("Nhập số token muốn đầu tư: "))
        if amount <= 0: raise ValueError
        players[idx]["fan_tokens"] += amount
        print(f"Thành công: Đã đầu tư {amount} token vào {players[idx]['player_id']}.")
        logging.info(f"Invested {amount} tokens into {players[idx]['player_id']}")
    except ValueError:
        print("Số token phải là số nguyên dương!")
        logging.warning("Invalid token input while investing")

def withdraw_tokens(players: List[Dict]) -> None:
    pid = input("Nhập mã tuyển thủ: ")
    idx = find_player_by_id(players, pid)
    if idx == -1: return 
    try:
        amount = int(input("Nhập số token muốn rút: "))
        if amount > players[idx]["fan_tokens"]:
            print("Không thể rút. Vượt quá số token hiện có.")
            logging.warning("Withdraw failed - Amount exceeds current fan tokens")
            return
        received = amount * 0.9
        players[idx]["fan_tokens"] -= amount
        print(f"Thành công: Thực nhận {received} token (đã trừ 10% phí).")
        logging.info(f"Withdrawn {amount} tokens from {pid}. Actual received: {received}")
    except ValueError:
        print("Lỗi nhập dữ liệu!")

def update_form(players: List[Dict]) -> None:
    pid = input("Nhập mã tuyển thủ: ")
    idx = find_player_by_id(players, pid)
    if idx == -1: return 
    try:
        new_form = float(input("Nhập hệ số mới (0.5 - 2.5): "))
        if not (0.5 <= new_form <= 2.5):
            print("Hệ số nằm ngoài khoảng 0.5 - 2.5")
            return 
        players[idx]["form_multiplier"] = new_form
        logging.info(f"Updated form multiplier for {pid} to {new_form}")
    except ValueError:
        print("Hệ số phải là số thực.")

def main():
    while True:
        print("\n===== HỆ THỐNG RIKKEI ESPORTS FANTASY =====")
        print("1. Xem sàn | 2. Đầu tư | 3. Rút vốn | 4. Cập nhật phong độ | 6. Thoát")
        choice = input("Chọn chức năng: ").strip()
        if choice == "1": display_market(players)
        elif choice == "2": invest_tokens(players)
        elif choice == "3": withdraw_tokens(players)
        elif choice == "4": update_form(players)
        elif choice == "6": break
        else: print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()