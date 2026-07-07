# TradeCalc
# Smart Calculator Telegram Bot (Professional Edition)  This is a modern, flexible, and professional Telegram Bot built with `aiogram 3.x`. It allows users to perform professional calculations based on their trade (e.g., Carpenter, Electrician) using a natural, step-by-step interactive interface.

## 🚀 Key Features
- **Dynamic Configuration:** Manage all professions, inputs, and formulas via a simple `config.json` file. No coding required to add new trades!
- **State-of-the-Art UX:** Interactive step-by-step input collection with "Back", "Next", and "Main Menu" navigation.
- **Robust Calculation Engine:** Uses a dynamic formula evaluator to process professional calculations instantly.
- **Production Ready:** Built with `AsyncIO` and `FSM` for high-performance, multi-user support.
- **Zero-Bug Design:** Implements strict error handling to ensure 100% stability.

- ## 🛠 Tech Stack
- **Python 3.10+**
- **Aiogram 3.x** (Asynchronous Telegram Bot API)
- **JSON** (For external configuration)

## 📦 How to Install
1. **Clone the repository.**
2. **Install requirements:** `pip install aiogram`
3. **Configure:** Open `config.json` and insert your Telegram Bot Token. Add your trades and formulas.
4. **Run:** `python main.py`

## 💼 Customization
To add a new trade, simply update the `config.json` file:
```json
"Plumber": {
    "inputs": ["pipes", "hours", "rate"],
    "formula": "(pipes * rate) + hours"
}
