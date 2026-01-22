from shogi_ai.ui.pvp import pvp
from shogi_ai.ui.vs_ai import vs_ai
from shogi_ai.ui.ai_vs_ai import ai_vs_ai

def main():
    print("対戦モードを選択してください：")
    print("1: PVPモード")
    print("2: AI対局モード")
    print("3: AI対AIモード")
    while True:
        choice = input(">")
        if choice == "1":
            pvp()
            break
        elif choice == "2":
            vs_ai()
            break
        elif choice == "3":
            ai_vs_ai()
            break
        else:
            print("正しく入力してください")

if __name__ == "__main__":
    main()