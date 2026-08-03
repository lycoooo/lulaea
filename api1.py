import requests
import time

api1 = "http://apk.hongda-pay.com/api/etcAccountForm/user_ping"
api2 = "http://apk.hongda-pay.com/api/etcAccountForm/getWebEtcAccountList"

headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; POCO X3 Build/QKQ1.200512.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/150.0.7871.181 Mobile Safari/537.36",
  'Accept': "application/json, text/plain, */*",
  'Accept-Encoding': "gzip, deflate",
  'Content-Length': "0",
  'Pragma': "no-cache",
  'Cache-Control': "no-cache",
  'gcash-token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJZCI6MCwiVVVJRCI6IiIsIlVpZCI6MCwiVXNlcm5hbWUiOiIiLCJOaWNrTmFtZSI6IiIsIkF1dGhvcml0eUlkIjowLCJJUCI6IiIsIkFnZW50VXNlcm5hbWUiOiIiLCJBZ2VudElkIjowLCJBdXRob3JpdGllcyI6bnVsbCwiTG9naW5JcFN0YXR1cyI6MCwiR29vZ2xlU2lnbiI6IiIsIlRpbWUiOjAsIkFkbWluSXBXaGl0ZVN0YXR1cyI6ZmFsc2UsIklwTGlzdCI6IiIsIlBhc3N3b3JkIjoiIiwiTGV2ZWwiOjAsIkJhc2VNYXAiOiJEazZ0SnVhNkV6M0gxV0c3a25KUmkvaW5QS3V6Q2NJM0VpdUNSUFpXNU04SGJlM001UG1odE92NzJCR0VrMzAvdjFNZGdUM2FSQmhmWFpkYTJGVWgwdis4MHVyV0R4bHNtUkU1VFhWQ25OdTVIK25ENFJmbVE4QkdDZlA0cnl0b3hRaGZJOW1wVDlaOHhuSEpGR1AwWW40Qlp3Q2ZWU0QySFZQNVpkNk03U1dHeGZaSE9ZVk5oMGM0YmJpd2VOQ2dVdy95NjhVWWJqZ3M5VHlESWFGZUdueURsTytrUUQySVowbStQK1BWanhuTmZrQloyUkFGcnhBMkZmWGdDdGhCVW1HMm1aQUdoM09YTHhIaFFlbVFrUEFYeG9ZSWdLV3NDY2I3Tkt4VjF5OVlHK3NjQVBKUUMycWxtRXpUR3FRdzZvTUM3dlZiZ2trdng5Z3VPekoxbkpEWnBMMk9NRXpVcHpsSFZhbTVCamQyeko0cFRhY3dCU0s2WWdTWnFiSEZ2V0lhYWxKQWl1NE5FQzMxc1EvZVBNRVJnV1V2MFM0bGxNdXRmN0I1NlRhYXpYSWVCNUl2TTRmVy9TVTltWlZqbExVaThuaEF3T1lUbHZsZFdJZnBENjhQUTdzMC9SMHNDMXUvbnVFRVZRTzRITlZqV25sREpaMFh6aHBjMFRxcDZqK055c0JlSGlyQ1lhcWJQV3VuVyszVDJGbmEvZFJBNkN6d0Fndk52aEY3eGM1OEJNVVhPcHFQcDRONHN2T1EiLCJCdWZmZXJUaW1lIjoxMDgwMCwiaXNzIjoicW1QbHVzR2Nhc2giLCJhdWQiOlsiR1ZBIl0sImV4cCI6MTc4NTc1NTc1MiwibmJmIjoxNzg1NzM0MTUyfQ.YZaxJlBtQA_kU5jWNk13Wwn_4BzbDs_ZrZrSMi0SVOM",
  'x-user-id': "0",
  'Origin': "http://apk.hongda-pay.com",
  'X-Requested-With': "com.hdpay137",
  'Referer': "http://apk.hongda-pay.com/card",
  'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
  'Cookie': "loginInfo={%22email%22:%22greyburn2020@gmail.com%22%2C%22password%22:%22200202%22%2C%22rememberPassword%22:true%2C%22i18n%22:%22zh-CN%22}; cardToken=N093YytDSHlHWTlNYzF3NlZjT0VpR09LS2VCUjBtaGNnb0NnWXpMY2FkU0N2and2TTgzTkY1WDhteDFsT0tEL0pLRm5RenZoU0xpREVtTzhvdnluSjZ1V09sUkwxSVVEMi9QTHVpSy96MVB6My9kdFFyQjNKYUJQZmROOVlmbEd6NC9lNS94VUpycER3b0o1OTI2TFpkVFJWQlhZQU5MYWYyVXBldlhzeWpOTWcxNy9rVUZoRExtVzB0L1NlME52; account=09942715322; gcash-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJZCI6MCwiVVVJRCI6IiIsIlVpZCI6MCwiVXNlcm5hbWUiOiIiLCJOaWNrTmFtZSI6IiIsIkF1dGhvcml0eUlkIjowLCJJUCI6IiIsIkFnZW50VXNlcm5hbWUiOiIiLCJBZ2VudElkIjowLCJBdXRob3JpdGllcyI6bnVsbCwiTG9naW5JcFN0YXR1cyI6MCwiR29vZ2xlU2lnbiI6IiIsIlRpbWUiOjAsIkFkbWluSXBXaGl0ZVN0YXR1cyI6ZmFsc2UsIklwTGlzdCI6IiIsIlBhc3N3b3JkIjoiIiwiTGV2ZWwiOjAsIkJhc2VNYXAiOiJEazZ0SnVhNkV6M0gxV0c3a25KUmkvaW5QS3V6Q2NJM0VpdUNSUFpXNU04SGJlM001UG1odE92NzJCR0VrMzAvdjFNZGdUM2FSQmhmWFpkYTJGVWgwdis4MHVyV0R4bHNtUkU1VFhWQ25OdTVIK25ENFJmbVE4QkdDZlA0cnl0b3hRaGZJOW1wVDlaOHhuSEpGR1AwWW40Qlp3Q2ZWU0QySFZQNVpkNk03U1dHeGZaSE9ZVk5oMGM0YmJpd2VOQ2dVdy95NjhVWWJqZ3M5VHlESWFGZUdueURsTytrUUQySVowbStQK1BWanhuTmZrQloyUkFGcnhBMkZmWGdDdGhCVW1HMm1aQUdoM09YTHhIaFFlbVFrUEFYeG9ZSWdLV3NDY2I3Tkt4VjF5OVlHK3NjQVBKUUMycWxtRXpUR3FRdzZvTUM3dlZiZ2trdng5Z3VPekoxbkpEWnBMMk9NRXpVcHpsSFZhbTVCamQyeko0cFRhY3dCU0s2WWdTWnFiSEZ2V0lhYWxKQWl1NE5FQzMxc1EvZVBNRVJnV1V2MFM0bGxNdXRmN0I1NlRhYXpYSWVCNUl2TTRmVy9TVTltWlZqbExVaThuaEF3T1lUbHZsZFdJZnBENjhQUTdzMC9SMHNDMXUvbnVFRVZRTzRITlZqV25sREpaMFh6aHBjMFRxcDZqK055c0JlSGlyQ1lhcWJQV3VuVyszVDJGbmEvZFJBNkN6d0Fndk52aEY3eGM1OEJNVVhPcHFQcDRONHN2T1EiLCJCdWZmZXJUaW1lIjoxMDgwMCwiaXNzIjoicW1QbHVzR2Nhc2giLCJhdWQiOlsiR1ZBIl0sImV4cCI6MTc4NTc1NTc1MiwibmJmIjoxNzg1NzM0MTUyfQ.YZaxJlBtQA_kU5jWNk13Wwn_4BzbDs_ZrZrSMi0SVOM"
}

params = {
    "page": 1,
    "pageSize": 10
}

last_api1 = 0
next_api2 = None


def debug_response(name, response):
    """Print useful information about the response."""
    print(f"\n----- {name} -----")
    print("Status Code :", response.status_code)
    print("URL         :", response.url)
    print("Content-Type:", response.headers.get("Content-Type"))

    text = response.text.strip()

    if not text:
        print("Response: <EMPTY>")
        return None

    try:
        return response.json()
    except ValueError:
        print("Response is NOT JSON.")
        print("-" * 60)
        print(text[:1000])  # Print first 1000 chars
        print("-" * 60)
        return None


while True:
    now = int(time.time())

    api1_wait = max(0, 20 - (now - last_api1))
    api2_wait = max(0, (next_api2 - now) if next_api2 else 0)

    print(
        f"\r[API1 in {api1_wait:>3}s]  [API2 in {api2_wait:>3}s]",
        end="",
        flush=True
    )

    # ===========================
    # API 1
    # ===========================
    if now - last_api1 >= 20:
        print()

        try:
            response1 = requests.post(
                api1,
                headers=headers,
                timeout=15
            )

            data1 = debug_response("API1", response1)

            if data1:
                d = data1.get("data", {})
                print(
                    f"[API1] "
                    f"code={data1.get('code')} | "
                    f"success={d.get('success')} | "
                    f"failed={d.get('failed')} | "
                    f"total={d.get('total')} | "
                    f"msg={data1.get('msg')}"
                )

        except requests.exceptions.RequestException as e:
            print("API1 Request Error:", e)

        last_api1 = now

    # ===========================
    # API 2
    # ===========================
    if next_api2 is None or now >= next_api2:
        print()

        try:
            response2 = requests.get(
                api2,
                params=params,
                headers=headers,
                timeout=15
            )

            data2 = debug_response("API2", response2)

            if data2:
                d = data2.get("data", {})

                print("=" * 60)
                print(
                    f"[API2] "
                    f"code={data2.get('code')} | "
                    f"msg={data2.get('msg')}"
                )

                print(
                    f"To be recharged: {d.get('to_be_recharged')}"
                )
                print(
                    f"Partial recharge: {d.get('partial_recharge')}"
                )
                print(
                    f"Success orders: {d.get('success_order')}"
                )
                print(
                    f"Fail orders: {d.get('fail_order')}"
                )
                print(
                    f"Incoming: {d.get('incoming_amount')}"
                )
                print(
                    f"Outgoing: {d.get('outgoing_amount')}"
                )
                print(
                    f"Total: {d.get('total_amount')}"
                )
                print(
                    f"Account amount: {d.get('total_account_amount')}"
                )

                for acc in d.get("list", []):
                    print(
                        f"Account: {acc.get('account')} | "
                        f"Status: {acc.get('status')} | "
                        f"Today Buy: {acc.get('todayBuy')} | "
                        f"Today Success: {acc.get('todaySuccessBuy')} | "
                        f"Success Money: {acc.get('todaySuccessMoney')} | "
                        f"Total Amount: {acc.get('totalAmount')}"
                    )

                print("=" * 60)

        except requests.exceptions.RequestException as e:
            print("API2 Request Error:", e)

        next_api2 = now + 90

    time.sleep(1)