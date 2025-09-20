import streamlit as st
import pandas as pd
import numpy as np

# ---- Custom CSS Styling with Background Image ----
st.markdown("""
    <style>
    body {
        background-image: url('https://images.unsplash.com/photo-1605902711622-cfb43c4437e1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .main {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 10px;
    }

    .css-18e3th9 {
        background-color: rgba(255, 255, 255, 0.9) !important;
    }

    h1 {
        color: #2c3e50;
    }

    h2, h3 {
        color: #34495e;
    }

    .stButton>button {
        background-color: #2e86de;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-size: 1em;
        margin-top: 10px;
    }

    .stTextInput>div>div>input {
        border: 1px solid #2e86de;
    }

    .stSelectbox>div>div {
        border: 1px solid #2e86de;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Helper Functions ----

def calculate_profit_loss(income, expenses):
    return income - expenses

def calculate_balance(transactions):
    return sum(transactions)

def calculate_tax(income):
    return income * 0.15  # 15% flat tax

# ---- Login Page ----

def show_login_page():
    st.title('🔐 Personal Finance - Login')
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button('Login'):
        if username == 'admin' and password == 'admin123':
            st.session_state.logged_in = True
            st.success('Login Successful!')
        else:
            st.error('Incorrect username or password')

# ---- Home Page ----

def show_home_page():
    st.title('💰 Personal Finance Dashboard')
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio("Go to", [
        "Profile", "Income & Expenses", "Investments",
        "Taxes", "Balance", "Transactions", "Chatbot"
    ])

    if page == "Profile":
        show_profile_page()
    elif page == "Income & Expenses":
        show_income_expenses_page()
    elif page == "Investments":
        show_investments_page()
    elif page == "Taxes":
        show_taxes_page()
    elif page == "Balance":
        show_balance_page()
    elif page == "Transactions":
        show_transactions_page()
    elif page == "Chatbot":
        show_chatbot_page()

# ---- Individual Pages ----

def show_profile_page():
    st.header("👤 User Profile")
    name = st.text_input("Enter your Name")
    email = st.text_input("Enter your Email")
    st.write(f"**Name:** {name}")
    st.write(f"**Email:** {email}")

def show_income_expenses_page():
    st.header("📈 Income & Expenses")
    income = st.number_input("Enter your monthly income", min_value=0.0)
    expenses = st.number_input("Enter your monthly expenses", min_value=0.0)

    profit_loss = calculate_profit_loss(income, expenses)
    st.write(f"### Profit/Loss: {profit_loss:.2f}")

    if profit_loss >= 0:
        st.success(f"✅ You are making a profit of {profit_loss:.2f}")
    else:
        st.warning(f"⚠️ You have a loss of {abs(profit_loss):.2f}")

def show_investments_page():
    st.header("💼 Investments")
    st.write("Track your investments and their returns.")

    investment_type = st.selectbox("Select investment type", [
        "Stocks", "Bonds", "Real Estate", "Cryptocurrency"
    ])
    amount = st.number_input(f"Amount invested in {investment_type}", min_value=0.0)
    rate_of_return = st.number_input(f"Annual rate of return for {investment_type} (%)", min_value=0.0)

    if amount > 0 and rate_of_return > 0:
        potential_value = amount * (1 + rate_of_return/100)
        st.success(f"📈 Estimated value after 1 year: {potential_value:.2f}")

def show_taxes_page():
    st.header("🧾 Taxes")
    income = st.number_input("Enter your income for tax calculation", min_value=0.0)

    if income > 0:
        tax = calculate_tax(income)
        st.info(f"💸 Estimated tax: {tax:.2f}")

def show_balance_page():
    st.header("💳 Balance Overview")
    transactions = st.text_area("Enter your recent transactions (comma separated)", value="1000,-500,200,-50")

    try:
        transactions_list = [float(x.strip()) for x in transactions.split(',')]
        balance = calculate_balance(transactions_list)
        st.success(f"📊 Your current balance: {balance:.2f}")
    except:
        st.error("Please enter valid numeric transactions separated by commas.")

def show_transactions_page():
    st.header("💵 Transactions")
    transaction_type = st.selectbox("Transaction Type", ["Deposit", "Withdrawal"])
    amount = st.number_input("Transaction Amount", min_value=0.0)

    if st.button("Add Transaction"):
        if transaction_type == "Deposit":
            st.success(f"✅ Deposited {amount:.2f} successfully!")
        else:
            st.success(f"✅ Withdrew {amount:.2f} successfully!")

# ---- Chatbot Feature ----

def show_chatbot_page():
    st.header("🤖 Chat with your Personal Finance Bot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def generate_bot_response(user_message):
        user_message = user_message.lower()

        if "income" in user_message:
            return "I can help you track your income. Enter it in the 'Income & Expenses' section!"
        elif "expenses" in user_message:
            return "You can log your expenses in the 'Income & Expenses' section!"
        elif "tax" in user_message:
            return "To calculate your taxes, go to the 'Taxes' section."
        elif "balance" in user_message:
            return "You can view your balance under the 'Balance Overview' section."
        elif "profit" in user_message or "loss" in user_message:
            return "Check the 'Income & Expenses' section to view your profit or loss."
        elif "investment" in user_message:
            return "Track your investments in the 'Investments' section."
        else:
            return "I'm sorry, I didn't quite understand that. Can you rephrase?"

    user_input = st.text_input("Ask me anything about your personal finance:")

    if user_input:
        bot_response = generate_bot_response(user_input)

        # Store chat history
        st.session_state.chat_history.append(f"**You:** {user_input}")
        st.session_state.chat_history.append(f"**Bot:** {bot_response}")

    # Display chat history
    for message in st.session_state.chat_history:
        st.markdown(message)

# ---- Main Script ----

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login_page()
else:
    show_home_page()
