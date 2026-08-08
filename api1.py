import requests
import time
import logging
import sys
import os
import threading
from flask import Flask

# Setup professional logging format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- DUMMY WEB SERVER FOR RENDER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Hongda-Pay Bot is running in the background and sending to Telegram! 🚀"

# --- YOUR ORIGINAL BOT CLASS ---
class HongdaPayClient:
    def __init__(self, email, password, tg_token, tg_chat_id):
        self.email = email
        self.password = password
        self.base_url = "http://apk.hongda-pay.com"
        
        # Telegram Setup
        self.tg_token = tg_token
        self.tg_chat_id = tg_chat_id
        
        self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; POCO X3 Build/QKQ1.200512.002; wv) AppleWebKit/537.36",
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate",
            'Pragma': "no-cache",
            'Cache-Control': "no-cache",
            'x-user-id': "0",
            'X-Requested-With': "com.hdpay137",
            'Origin': self.base_url,
            'Referer': f"{self.base_url}/card",
            'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
        })
        
        self.session.cookies.set('cardToken', 'N093YytDSHlHWTlNYzF3NlZjT0VpR09LS2VCUjBtaGNnb0NnWXpMY2FkU0N2and2TTgzTkY1WDhteDFsT0tEL0pLRm5RenZoU0xpREVtTzhvdnluSjZ1V09sUkwxSVVEMi9QTHVpSy96MVB6My9kdFFyQjNKYUJQZmROOVlmbEd6NC9lNS94VUpycER3b0o1OTI2TFpkVFJWQlhZQU5MYWYyVXBldlhzeWpOTWcxNy9rVUZoRExtVzB0L1NlME52')
        self.session.cookies.set('account', '09942715322')
        self.session.cookies.set('loginInfo', '{"email":"greyburn2020@gmail.com","password":"200202","rememberPassword":true,"i18n":"zh-CN"}')

    def send_telegram_msg(self, text, use_monospace=False):
        """Sends a message to the specified Telegram Chat."""
        if not self.tg_chat_id or self.tg_chat_id == "YOUR_CHAT_ID_HERE":
            logging.warning("Telegram CHAT_ID not set. Skipping Telegram notification.")
            return

        url = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
        
        if use_monospace:
            text = f"<pre>{text}</pre>"
            
        payload = {
            "chat_id": self.tg_chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send Telegram message: {e}")

    def login(self):
        url = f"{self.base_url}/api/base/web/login"
        payload = {
            "email": self.email,
            "password": self.password,
            "rememberPassword": True,
            "i18n": "zh-CN"
        }
        
        logging.info("Attempting to log in and fetch fresh token (API 1)...")
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status() 
            data = response.json()
            
            token = data.get("data", {}).get("token", "")
            if not token:
                logging.error("Login successful but token not found in response.")
                return False
            
            self.session.headers.update({'gcash-token': token})
            self.session.cookies.set('gcash-token', token)
            
            logging.info("Successfully retrieved and applied new token.")
            self.send_telegram_msg("🔄 <b>System Update:</b> Successfully logged in and refreshed token!")
            return True
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Login failed: {e}")
            self.send_telegram_msg(f"❌ <b>Login Failed:</b> {e}")
            return False

    def get_account_list(self, retry=True):
        url = f"{self.base_url}/api/etcAccountForm/getWebEtcAccountList"
        params = {'page': "1", 'pageSize': "10"}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            json_data = response.json()
            
            # --- CODE 7 CHECK FOR API 2 ---
            if json_data.get("code") == 7:
                if retry:
                    logging.warning("⚠️ API 2: Token expired (Code 7 detected). Re-authenticating...")
                    if self.login():
                        return self.get_account_list(retry=False)
                else:
                    logging.error("❌ API 2: Token refresh failed.")
                    return

            data = json_data.get("data", {})
            accounts = data.get("list", [])
            
            # --- ULTRA-PRO TELEGRAM DASHBOARD DESIGN ---
            msg = "⚡ <b>FINANCIAL OPERATIONS DASHBOARD</b> ⚡\n"
            msg += "━━━━━━━━━━━━━━━━━━━━━━━\n"
            msg += f"🌐 <b>System Overview</b>\n"
            msg += f"• Total Accounts Active: <code>{data.get('total', 0)}</code>\n"
            msg += f"• Incoming Vol: <code>₱{data.get('incoming_amount', 0):,}</code>\n"
            msg += f"• Outgoing Vol: <code>₱{abs(data.get('outgoing_amount', 0)):,}</code>\n"
            msg += f"• Net Balance: <code>₱{data.get('total_amount', 0):,}</code>\n"
            msg += f"• Account Pool Val: <code>₱{data.get('total_account_amount', 0):,}</code>\n"
            msg += f"• Queue State: Recharged ({data.get('to_be_recharged', 0)}) | Partial ({data.get('partial_recharge', 0)})\n"
            msg += "━━━━━━━━━━━━━━━━━━━━━━━\n"
            msg += f"📋 <b>Active Accounts Report</b>\n"
            
            if accounts:
                for index, acc in enumerate(accounts, 1):
                    msg += f"\n<b>#{index} 📱 <code>{acc.get('account')}</code></b>\n"
                    msg += f"├ Status: <code>{acc.get('status', 'N/A')}</code> | Device: <code>{acc.get('deviceStatus', 'N/A')}</code>\n"
                    msg += f"├ <b>Today Performance:</b>\n"
                    msg += f"│  • Buy Volume: <code>{acc.get('todayBuy')}</code> (Success: <b>{acc.get('todaySuccessBuy')}</b>)\n"
                    msg += f"│  • Success Revenue: <code>₱{acc.get('todaySuccessMoney', 0):,}</code>\n"
                    msg += f"├ <b>Monthly Metrics:</b>\n"
                    msg += f"│  • Success Buys: <code>{acc.get('moonSuccessBuy')}</code>\n"
                    msg += f"│  • Success Payout: <code>₱{acc.get('moonSuccessMoney', 0):,}</code>\n"
                    msg += f"└ <b>Limits & Reserves:</b>\n"
                    msg += f"   • <b>Account Balance (Total Amount): <code>₱{acc.get('totalAmount', 0):,}</code></b>\n"
                    msg += f"   • Today Limit Left: <code>₱{acc.get('paymentTodayLimitMoney', 0):,}</code>\n"
                    msg += f"   • Month Limit OK: <code>₱{acc.get('paymentMoonLimitSuccessMoney', 0):,}</code>\n"
                    msg += f"   • Incoming Pool: <code>₱{acc.get('incomingAmount', 0):,}</code>\n"
            else:
                msg += "⚠️ No active accounts reporting.\n"
                
            logging.info("✅ API 2 Processed & Formatted Successfully")
            self.send_telegram_msg(msg, use_monospace=False)
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API 2 failed: {e}")
        except ValueError:
            logging.error("API 2 returned invalid JSON data.")

    def ping_user(self, retry=True):
        url = f"{self.base_url}/api/etcAccountForm/user_ping"
        
        try:
            response = self.session.post(url)
            response.raise_for_status()
            json_data = response.json()
            
            # --- CODE 7 CHECK FOR API 3 ---
            if json_data.get("code") == 7:
                if retry:
                    logging.warning("⚠️ API 3: Token expired (Code 7 detected). Re-authenticating...")
                    if self.login():
                        return self.ping_user(retry=False)
                else:
                    logging.error("❌ API 3: Token refresh failed.")
                    return

            data = json_data.get("data", {})
            success = data.get("success", 0)
            failed = data.get("failed", 0)
            total = data.get("total", 0)
            
            ping_stats = f"📡 <b>PING STATUS</b>\nTotal: {total} | Success: {success} | Failed: {failed}"
            logging.info(f"✅ API 3: Total: {total} | Success: {success} | Failed: {failed}")
            
            self.send_telegram_msg(ping_stats)
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API 3 failed: {e}")
        except ValueError:
            logging.error("API 3 returned invalid JSON data.")

    def start_loop(self, interval=50):
        logging.info(f"Starting background loop every {interval} seconds...\n")
        self.send_telegram_msg("🟢 <b>Bot Started:</b> Beginning tracking loop.")
        while True:
            self.get_account_list()
            self.ping_user()
            
            for remaining in range(interval, 0, -1):
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                sys.stdout.write(f"\r{timestamp} [INFO] Next update in: {remaining:02d} seconds... ")
                sys.stdout.flush()
                time.sleep(1)
            
            sys.stdout.write("\n")

# --- BACKGROUND THREAD RUNNER ---
def run_bot_in_background():
    TG_TOKEN = "8919242938:AAH-5Ent8nmbtP_-O-K0RmzbDAhGuzl5nnw"
    TG_CHAT_ID = "5295241896"
    
    client = HongdaPayClient("greyburn2020@gmail.com", "200202", TG_TOKEN, TG_CHAT_ID)
    if client.login():
        client.start_loop(interval=50)
    else:
        logging.error("Bot thread terminated due to initial login failure.")

# ==========================================
# Script Execution
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    logging.info(f"🚀 Render is looking for port: {port}")
    
    logging.info("Starting bot background thread...")
    bot_thread = threading.Thread(target=run_bot_in_background, daemon=True)
    bot_thread.start()
    
    logging.info(f"Starting Flask web server on 0.0.0.0:{port}...")
    app.run(host='0.0.0.0', port=port)
