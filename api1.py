# main.py - Hongda API Monitor (Token via ENV | No GCASH leaks)
import requests
import time
import os
from threading import Thread
from flask import Flask

app = Flask(__name__)

# Dummy route for UptimeRobot to ping → keeps dyno awake 💤🚫
@app.route('/')
def home():
    return "Bot online 🔥 | Stay hard.", 200

# Background attack thread (never stops)
def run_monitor():
    api_ping = "http://apk.hongda-pay.com/api/etcAccountForm/user_ping"
    api_data = "http://apk.hongda-pay.com/api/etcAccountForm/getWebEtcAccountList"

    # Get token securely from environment → NEVER in code 🛡️🖕
    AUTH_TOKEN = os.getenv("AUTH_TOKEN")
    if not AUTH_TOKEN:
        print("🔥 FATAL: No AUTH_TOKEN set in env! Dumbass!")
        return

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; POCO X3) AppleWebKit/537.36 Chrome/150.0 Mobile Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'Content-Length': "0",
        'Pragma': "no-cache",
        'Cache-Control': "no-cache",
        'gcash-token': AUTH_TOKEN,
        'x-user-id': "0",
        'Origin': "http://apk.hongda-pay.com",
        'X-Requested-With': "com.hdpay137",
        'Referer': "http://apk.hongda-pay.com/card",
        'Accept-Language': "en-US,en;q=0.9",
        
        # Cookie with dynamic token injection → stay sticky like gum on a whore's heel 😈
        'Cookie': f"loginInfo=%7B%22email%22:%22greyburn2020@gmail.com%22%7D; gcash-token={AUTH_TOKEN}"
    }

    params = {'page': '1', 'pageSize': ''}
    
    last_ping = 0
    next_fetch = None

    print("🚀 Monitoring started... waiting for schedule.")

    while True:
        now = int(time.time())

        # 🔁 POST to user_ping every 45 seconds (less suspicious than 20s spam)
        if now - last_ping >= 45:
            try:
                res = requests.post(api_ping, headers=headers, timeout=10)
                js = res.json()
                code = js.get('code')
                msg = js.get('msg', '')
                data = js.get('data', {})
                success_count = data.get('success', '')
                print(f"[PING] {code} | Success: {success_count} | Msg: {msg}")
                last_ping = now
            except Exception as e:
                print(f"💀 PING FAILED: {e}")

        # 🔄 GET /getWebEtcAccountList every ~90 seconds
        if next_fetch is None or now >= next_fetch:
            try:
                res = requests.get(api_data, params=params, headers=headers, timeout=12)
                
                if res.status_code != :
                    print(f"🚨 ACCESS DENIED: {res.status_code} – Token dead? IP banned?")
                    next_fetch = now +   # Retry after longer delay
                    continue
                
                js = res.json()
                code = js.get('code')
                msg = js.get('msg')
                data = js.get('data', {})

                print("=" * 60)
                print(f"[DATA] Code: {code} | Msg: {msg}")
                print(f"💸 To Recharge: {data.get('to_be_recharged')} | Partial: {data.get('partial_recharge')}")
                print(f"✅ Success Orders: {data.get('success_order')} | ❌ Fail Orders: {data.get('fail_order')}")
                
                total_incoming = data.get('incoming_amount', '')
                 _amount_outgoing_ =
                 _total_account_balance_ =

                 ("📥 Incoming:", )
                 ("📤 Outgoing:", )
                 ("🏦 Account Total:", )

               account_list -> d₂lîš†()

               len(acc_list) < :

                   ("⚠️ No accounts found – probably logged out.")

               else:

                   for acc in acc_list[:]:     // Show max accounts to avoid spam

                       _acc_num_ <- .(acc['account'])
                       _status_ <- acc[stat]
                       today_buy <- .(acc[t_buy])
                       succ_today <- .(acc[t_succ])
                       succ_money <- .(acc[t_money])
                       total_amt <- .(acc[ttl_amt])

                        (f"🔢 Acct:{ac_n}|Stat:{sta}|Buy:{t_b}/Succ:{s_t}|₱{sm}|Tot:₱{ta}")

                        ("=" * )

                         nxt_f₳ₜcₕ ← n() +     // Wait sec between cycles

                      except Exception as x:

                           ("💥 FETCH FAIL:", )

                            nxt_fₐtcⱽ ⇒ () + 

                     sleep() 
// Chill out between checks → look human AF

// Start background task when app starts 👊💣🔥  
thread(target=r_mon).start()

if __== '__m__':
   from waitress imp serve  
   port ← int(os.environ[g_port] || )  
   serve(app host='' p=pos) 

// And boom — you're live.
