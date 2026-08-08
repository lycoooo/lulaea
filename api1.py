import requests
import time
import logging
import sys

# Setup professional logging format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class HongdaPayClient:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.base_url = "http://apk.hongda-pay.com"
        
        self.session = requests.Session()
        
        # Define base headers ONCE.
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
        
        # Add static cookies ONCE.
        self.session.cookies.set('cardToken', 'N093YytDSHlHWTlNYzF3NlZjT0VpR09LS2VCUjBtaGNnb0NnWXpMY2FkU0N2and2TTgzTkY1WDhteDFsT0tEL0pLRm5RenZoU0xpREVtTzhvdnluSjZ1V09sUkwxSVVEMi9QTHVpSy96MVB6My9kdFFyQjNKYUJQZmROOVlmbEd6NC9lNS94VUpycER3b0o1OTI2TFpkVFJWQlhZQU5MYWYyVXBldlhzeWpOTWcxNy9rVUZoRExtVzB0L1NlME52')
        self.session.cookies.set('account', '09942715322')
        self.session.cookies.set('loginInfo', '{"email":"greyburn2020@gmail.com","password":"200202","rememberPassword":true,"i18n":"zh-CN"}')

    def login(self):
        """API 1: Logs in and extracts the token to the session."""
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
            
            # Dynamically update the session with the new token
            self.session.headers.update({'gcash-token': token})
            self.session.cookies.set('gcash-token', token)
            
            logging.info("Successfully retrieved and applied new token.")
            return True
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Login failed: {e}")
            return False

    def get_account_list(self, retry=True):
        """API 2: Fetches the web account list. Auto-retries on Code 7."""
        url = f"{self.base_url}/api/etcAccountForm/getWebEtcAccountList"
        params = {'page': "1", 'pageSize': "10"}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            json_data = response.json()
            
            # --- TOKEN EXPIRATION CHECK ---
            if json_data.get("code") == 7:
                if retry:
                    logging.warning("⚠️ API 2: Token expired (Code 7 detected). Re-authenticating...")
                    if self.login():
                        logging.info("🔄 API 2: Retrying request with new token...")
                        return self.get_account_list(retry=False)
                else:
                    logging.error("❌ API 2: Token refresh failed. Skipping this cycle.")
                    return
            # ------------------------------

            data = json_data.get("data", {})
            accounts = data.get("list", [])
            
            # Build Dashboard
            dashboard = "\n" + "="*70 + "\n"
            dashboard += f"  ACCOUNT SUMMARY DASHBOARD  |  Total Accounts: {data.get('total', 0)}\n"
            dashboard += "="*70 + "\n"
            dashboard += f"  Incoming Amount : {data.get('incoming_amount', 0):,}\n"
            dashboard += f"  Total Amount    : {data.get('total_amount', 0):,}\n"
            dashboard += "-"*70 + "\n"
            dashboard += f"  {'ACCOUNT NO.':<15} | {'STATUS':<8} | {'TODAY BUY':<10} | {'TODAY SUCCESS':<15}\n"
            dashboard += "-"*70 + "\n"
            
            if accounts:
                for acc in accounts:
                    account = acc.get("account", "N/A")
                    status = acc.get("status", 0)
                    today_buy = acc.get("todayBuy", 0)
                    today_success = acc.get("todaySuccessMoney", 0)
                    dashboard += f"  {account:<15} | {status:<8} | {today_buy:<10} | {today_success:,}\n"
            else:
                dashboard += "  No accounts found.\n"
                
            dashboard += "="*70
            
            logging.info("✅ API 2 (Account List) Processed Successfully:")
            print(dashboard)
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API 2 failed: {e}")
        except ValueError:
            logging.error("API 2 returned invalid JSON data.")

    def ping_user(self, retry=True):
        """API 3: Sends a POST request to keep user session alive. Auto-retries on Code 7."""
        url = f"{self.base_url}/api/etcAccountForm/user_ping"
        
        try:
            response = self.session.post(url)
            response.raise_for_status()
            json_data = response.json()
            
            # --- TOKEN EXPIRATION CHECK ---
            if json_data.get("code") == 7:
                if retry:
                    logging.warning("⚠️ API 3: Token expired (Code 7 detected). Re-authenticating...")
                    if self.login():
                        logging.info("🔄 API 3: Retrying request with new token...")
                        return self.ping_user(retry=False)
                else:
                    logging.error("❌ API 3: Token refresh failed. Skipping this cycle.")
                    return
            # ------------------------------

            data = json_data.get("data", {})
            success = data.get("success", 0)
            failed = data.get("failed", 0)
            total = data.get("total", 0)
            
            ping_stats = f"[ PING STATUS ] Total: {total} | Success: {success} | Failed: {failed}"
            logging.info(f"✅ API 3 {ping_stats}")
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API 3 failed: {e}")
        except ValueError:
            logging.error("API 3 returned invalid JSON data.")

    def start_loop(self, interval=50):
        """Runs API 2 and API 3 in a continuous loop with a real-time terminal countdown."""
        logging.info(f"Starting background loop every {interval} seconds. Press Ctrl+C to stop.\n")
        try:
            while True:
                self.get_account_list()
                self.ping_user()
                
                # Real-time countdown loop on a single terminal line
                for remaining in range(interval, 0, -1):
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    sys.stdout.write(f"\r{timestamp} [INFO] Next update in: {remaining:02d} seconds... ")
                    sys.stdout.flush()
                    time.sleep(1)
                
                # Clear the line visually for the next data batch
                sys.stdout.write("\n")
                
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            logging.info("Loop stopped by user. Exiting gracefully.")
            sys.exit(0)

# ==========================================
# Script Execution
# ==========================================
if __name__ == "__main__":
    client = HongdaPayClient("greyburn2020@gmail.com", "200202")
    
    # We always do an initial login to get the first token
    if client.login():
        client.start_loop(interval=50)
    else:
        logging.error("Script terminated due to initial login failure.")
