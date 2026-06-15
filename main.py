import logging
from typing import List, Dict, Optional

# Cấu hình logging
logging.basicConfig(
    filename='fantasy_league.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def find_player_by_id(players: List[Dict], player_id: str) -> Optional[int]:
    """Tìm index của tuyển thủ trong danh sách dựa trên ID (chuẩn hóa hoa)."""
    player_id = player_id.strip().upper()
    for index, p in enumerate(players):
        if p.get("player_id", "").upper() == player_id:
            return index
    return None

def display_market(players: List[Dict]) -> None:
    """Hiển thị sàn giao dịch tuyển thủ."""
    if not players:
        print("Sàn giao dịch hiện chưa có tuyển thủ nào.")
        return
    
    print("\n--- SÀN GIAO DỊCH TUYỂN THỦ ---")
    print(f"{'ID':<10} | {'Tên tuyển thủ':<15} | {'Giá trị':<10} | {'Fan Token':<10} | {'Điểm trận':<10} | {'Hệ số':<6} | {'Trạng thái'}")
    print("-" * 90)
    
    for p in players:
        tokens = p.get("fan_tokens", 0)
        if tokens == 0: status = "Chưa có người đầu tư"
        elif tokens <= 1000: status = "Đang thu hút"
        else: status = "Tuyển thủ Hot"
        
        print(f"{p.get('player_id', 'N/A'):<10} | {p.get('name', 'Unknown'):<15} | "
              f"{p.get('market_value', 0):<10} | {tokens:<10} | "
              f"{p.get('match_points', 0):<10} | {p.get('form_multiplier', 1.0):<6} | {status}")
    
    logging.info("User viewed the player market.")

def invest_tokens(players: List[Dict]) -> None:
    """Đầu tư Fan Token vào tuyển thủ."""
    m_id = input("Nhập mã tuyển thủ: ")
    idx = find_player_by_id(players, m_id)
    if idx is None:
        print("Không tìm thấy tuyển thủ!")
        logging.warning(f"Invest failed - Player {m_id.upper()} not found")
        return

    try:
        amount = int(input("Nhập số token muốn đầu tư: "))
        if amount <= 0: raise ValueError
        players[idx]["fan_tokens"] += amount
        print(f"Thành công: Đã đầu tư {amount} token vào tuyển thủ {players[idx]['player_id']}.")
        print(f"Số Fan Token hiện tại của {players[idx]['name']}: {players[idx]['fan_tokens']}")
        logging.info(f"Invested {amount} tokens into {players[idx]['player_id']}")
    except ValueError:
        print("Số token phải là số nguyên dương. Vui lòng nhập lại.")
        logging.warning("Invalid token input while investing")

def withdraw_tokens(players: List[Dict]) -> None:
    """Rút vốn từ tuyển thủ (trừ 10% phí)."""
    m_id = input("Nhập mã tuyển thủ: ")
    idx = find_player_by_id(players, m_id)
    if idx is None:
        print("Không tìm thấy tuyển thủ!")
        return

    try:
        amount = int(input("Nhập số token muốn rút: "))
        if amount > players[idx]["fan_tokens"]:
            print(f"Không thể rút. Số token muốn rút vượt quá số Fan Token hiện có.\nFan Token hiện có của {players[idx]['name']}: {players[idx]['fan_tokens']}")
            logging.warning("Withdraw failed - Amount exceeds current fan tokens")
            return
        
        fee = amount * 0.1
        actual_received = amount - fee
        players[idx]["fan_tokens"] -= amount
        print(f"Thành công: Đã rút {amount} token khỏi tuyển thủ {players[idx]['player_id']}.")
        print(f"Phí giao dịch 10%: {fee} token\nSố token thực nhận về ví: {actual_received} token")
        logging.info(f"Withdrawn {amount} tokens from {players[idx]['player_id']}. Actual received: {actual_received}")
    except ValueError:
        print("Số token không hợp lệ.")

def update_form(players: List[Dict]) -> None:
    """Cập nhật hệ số phong độ."""
    m_id = input("Nhập mã tuyển thủ: ")
    idx = find_player_by_id(players, m_id)
    if idx is None: return

    try:
        new_form = float(input("Nhập hệ số phong độ mới (0.5 - 2.5): "))
        if not (0.5 <= new_form <= 2.5):
            print("Hệ số phong độ chỉ được nằm trong khoảng 0.5 đến 2.5.")
            return
        players[idx]["form_multiplier"] = new_form
        print(f"Thành công: Đã cập nhật hệ số phong độ cho {players[idx]['name']}. Hệ số mới: x{new_form}")
        logging.info(f"Updated form multiplier for {players[idx]['player_id']} to {new_form}")
    except ValueError:
        print("Hệ số phong độ phải là số thực.")

def calculate_match_points(players: List[Dict]) -> None:
    """Chấm điểm sau trận đấu."""
    m_id = input("Nhập mã tuyển thủ: ")
    idx = find_player_by_id(players, m_id)
    if idx is None:
        print("Không tìm thấy tuyển thủ!")
        return

    try:
        base_points = float(input("Nhập điểm gốc của trận đấu: "))
        earned = base_points * players[idx]["form_multiplier"]
        players[idx]["match_points"] += earned
        print(f">> Tuyển thủ {players[idx]['name']} nhận được {earned} điểm (Hệ số x{players[idx]['form_multiplier']}).")
        print(f"Tổng điểm: {players[idx]['match_points']}")
        logging.info(f"Added {earned} match points to {players[idx]['player_id']}")
    except ValueError:
        print("Điểm không hợp lệ.")

def main():
    players = [
        {"player_id": "T101", "name": "Faker", "market_value": 5000, "fan_tokens": 1500, "match_points": 0, "form_multiplier": 1.0},
        {"player_id": "GEN01", "name": "Chovy", "market_value": 4800, "fan_tokens": 800, "match_points": 500, "form_multiplier": 1.2}
    ]
    
    while True:
        print("\n===== HỆ THỐNG RIKKEI ESPORTS FANTASY =====")
        print("1. Xem Sàn Giao Dịch\n2. Đầu tư Fan Token\n3. Rút vốn\n4. Biến động phong độ\n5. Chấm điểm\n6. Thoát")
        choice = input("Chọn chức năng (1-6): ")
        if choice == '1': display_market(players)
        elif choice == '2': invest_tokens(players)
        elif choice == '3': withdraw_tokens(players)
        elif choice == '4': update_form(players)
        elif choice == '5': calculate_match_points(players)
        elif choice == '6':
            print("Đóng hệ thống Rikkei Esports Fantasy.")
            logging.info("System closed.")
            break

if __name__ == "__main__":
    main()