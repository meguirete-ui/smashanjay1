import streamlit as st
import asyncio
import os
import json
import random
import re
import time
import shutil
import string
from datetime import datetime, timezone
from twikit import Client

# --- CONFIG ---
st.set_page_config(
    page_title="Wurk Ultimate Web (Safe Mode)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

SESSION_DIR = 'sessions'
if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)

# USER AGENT (Chrome Windows)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

# --- UTILS ---
def get_client():
    return Client('en-US', user_agent=USER_AGENT)

def get_sessions():
    return [f.replace('.json', '') for f in os.listdir(SESSION_DIR) if f.endswith('.json')]

def extract_id(text):
    match = re.search(r'status/(\d+)', text)
    if match: return match.group(1)
    return text if text.isdigit() else None

def generate_magic_string(length=4):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def calculate_account_age(created_at_str):
    try:
        if isinstance(created_at_str, str):
            dt = datetime.strptime(created_at_str, '%a %b %d %H:%M:%S %z %Y')
        else:
            dt = created_at_str
        now = datetime.now(timezone.utc)
        days = (now - dt).days
        if days < 30: return f"{days} Hari"
        elif days < 365: return f"{days // 30} Bulan"
        else: return f"{days // 365} Tahun"
    except: return "-"

# --- ASYNC WRAPPERS ---
async def login_process(username, auth, ct0):
    client = get_client()
    cookies = {"auth_token": auth.strip(), "ct0": ct0.strip()}
    with open('temp_web.json', 'w') as f: json.dump(cookies, f)
    try:
        client.load_cookies('temp_web.json')
        user = await client.get_user_by_screen_name(username)
        client.save_cookies(os.path.join(SESSION_DIR, f"{user.screen_name}.json"))
        return True, f"Login sukses: @{user.screen_name}"
    except Exception as e:
        return False, str(e)
    finally:
        if os.path.exists('temp_web.json'): os.remove('temp_web.json')

async def raid_process(accounts, target_id, actions, min_d, max_d):
    log_data = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, acc in enumerate(accounts):
        status_text.text(f"Processing @{acc} ({i+1}/{len(accounts)})...")
        worker = get_client()
        result = {"User": f"@{acc}", "RT": "➖", "Like": "➖", "Follow": "➖", "Status": "OK"}
        
        try:
            worker.load_cookies(os.path.join(SESSION_DIR, f"{acc}.json"))
            
            if "RT" in actions:
                try: await worker.retweet(target_id); result["RT"] = "✅"
                except Exception as e: 
                    if "429" in str(e): return log_data, "RATE LIMIT KENA! BERHENTI SEKARANG."
                    result["RT"] = "❌"
            
            if "Like" in actions:
                try: await worker.favorite_tweet(target_id); result["Like"] = "✅"
                except: result["Like"] = "❌"
                
            if "Follow" in actions:
                try: 
                    t = await worker.get_tweet_by_id(target_id)
                    if t and t.user: await t.user.follow(); result["Follow"] = "✅"
                    else: result["Follow"] = "⚠"
                except: result["Follow"] = "❌"
                
        except Exception as e:
            result["Status"] = "Login Fail"
        
        log_data.append(result)
        progress_bar.progress((i + 1) / len(accounts))
        
        # DELAY SAFETY
        if i < len(accounts) - 1:
            delay = random.uniform(min_d, max_d) # Pake float biar lebih human
            time.sleep(delay)
                
    status_text.text("Raid Selesai!")
    return log_data, "Sukses"

async def scrape_process(target_user, limit, mode):
    scraper = get_client()
    sessions = get_sessions()
    if not sessions: return None, "Tidak ada akun login"
    
    try:
        scraper.load_cookies(os.path.join(SESSION_DIR, f"{sessions[0]}.json"))
        user = await scraper.get_user_by_screen_name(target_user)
        
        data = []
        fetch_func = user.get_followers if mode == "Followers" else user.get_following
        
        try:
            batch = await fetch_func(count=40)
            data.extend(batch)
            
            # Pagination dengan Delay Lebih Lama
            while len(data) < limit and batch.next_cursor:
                delay = random.uniform(2.5, 5.5) # Delay acak 2.5 - 5.5 detik per page
                time.sleep(delay) 
                batch = await batch.next()
                if not batch: break
                data.extend(batch)
        except Exception as e:
            if "429" in str(e):
                return None, "RATE LIMIT (429)! Twitter memblokir sementara. Ganti IP atau tunggu 15 menit."
            else:
                return None, f"Error saat fetch: {e}"
            
        # Format Data
        formatted = []
        for u in data[:limit]:
            formatted.append({
                "Username": u.screen_name,
                "Name": u.name,
                "Umur Akun": calculate_account_age(u.created_at),
                "Joined": str(u.created_at),
                "Followers": u.followers_count
            })
        return formatted, f"Sukses ambil {len(formatted)} data"
            
    except Exception as e:
        return None, str(e)

async def check_health_process(usernames):
    checker = get_client()
    sessions = get_sessions()
    if not sessions: return []
    checker.load_cookies(os.path.join(SESSION_DIR, f"{sessions[0]}.json"))
    
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, uname in enumerate(usernames):
        uname = uname.strip().replace('@', '')
        status_text.text(f"Checking {uname}...")
        res = {"User": f"@{uname}", "Status": "UNKNOWN"}
        
        try:
            u = await checker.get_user_by_screen_name(uname)
            res["Status"] = "LOCKED" if u.protected else "ACTIVE"
        except Exception as e:
            err = str(e).lower()
            if "429" in err:
                st.error("RATE LIMIT TERCAPAI! Stop checking.")
                break
            if "suspend" in err: res["Status"] = "SUSPENDED"
            elif "not found" in err or "404" in err: res["Status"] = "NOT FOUND"
            else: res["Status"] = "ERROR"
        
        results.append(res)
        progress_bar.progress((i + 1) / len(usernames))
        
        # Delay Safety Check
        time.sleep(random.uniform(1.5, 3.0)) 
        
    return results

# --- UI LAYOUT ---

st.sidebar.title("⚡ Wurk Ultimate")
menu = st.sidebar.radio("Navigasi", ["Dashboard", "Raid Assistant", "Scraper Pro", "Health Checker", "Akun Manager"])

if menu == "Dashboard":
    st.title("Dashboard Utama")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Akun Tersimpan", len(get_sessions()))
    with col2:
        st.info("Selamat datang di Wurk Ultimate Web Edition (Safe Mode).")
        st.code(f"Session Path: {os.path.abspath(SESSION_DIR)}")

elif menu == "Akun Manager":
    st.title("Manajemen Akun")
    
    tab1, tab2, tab3 = st.tabs(["Tambah Akun", "Daftar Akun", "Backup/Restore"])
    
    with tab1:
        st.write("Login menggunakan Cookies (F12 > Application > Cookies)")
        with st.form("login_form"):
            u_name = st.text_input("Username (Tanpa @)")
            auth = st.text_input("auth_token", type="password")
            ct0 = st.text_input("ct0", type="password")
            submitted = st.form_submit_button("Simpan Akun")
            
            if submitted:
                if u_name and auth and ct0:
                    with st.spinner("Verifikasi Login..."):
                        success, msg = asyncio.run(login_process(u_name, auth, ct0))
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("Isi semua data!")

    with tab2:
        sessions = get_sessions()
        if sessions:
            st.success(f"{len(sessions)} Akun Terdeteksi")
            st.table(sessions)
            if st.button("Hapus Semua Akun (Reset)"):
                for f in os.listdir(SESSION_DIR):
                    os.remove(os.path.join(SESSION_DIR, f))
                st.rerun()
        else:
            st.warning("Belum ada akun.")

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📦 Export Sessions (ZIP)"):
                if os.listdir(SESSION_DIR):
                    shutil.make_archive('sessions_backup', 'zip', SESSION_DIR)
                    with open("sessions_backup.zip", "rb") as fp:
                        st.download_button("Download Backup", fp, "sessions_backup.zip")
                else: st.error("Tidak ada akun.")
        
        with col2:
            uploaded = st.file_uploader("Upload Backup (ZIP)", type="zip")
            if uploaded and st.button("Restore"):
                with open("temp_restore.zip", "wb") as f:
                    f.write(uploaded.getbuffer())
                shutil.unpack_archive("temp_restore.zip", SESSION_DIR)
                os.remove("temp_restore.zip")
                st.success("Restore Berhasil!")

elif menu == "Raid Assistant":
    st.title("🚀 Wurk Raid Assistant")
    sessions = get_sessions()
    if not sessions:
        st.error("Silakan tambah akun dulu di menu Akun Manager!")
        st.stop()

    col1, col2 = st.columns([2, 1])
    with col1:
        target_link = st.text_input("Link Tweet Target")
        target_id = extract_id(target_link)
        if target_id: st.caption(f"Target ID: {target_id}")
    
    with col2:
        st.write("Template Aksi:")
        do_rt = st.checkbox("Retweet", value=True)
        do_like = st.checkbox("Like", value=True)
        do_follow = st.checkbox("Follow Author", value=False)
    
    st.divider()
    sp_col1, sp_col2, sp_col3 = st.columns(3)
    with sp_col1:
        limit = st.number_input("Jumlah Akun", 1, len(sessions), len(sessions))
    with sp_col2:
        min_d = st.number_input("Min Delay (detik)", 1, 60, 10)
    with sp_col3:
        max_d = st.number_input("Max Delay (detik)", 1, 120, 20)
        
    if st.button("🔥 MULAI RAID", type="primary"):
        if not target_id:
            st.error("Link tweet tidak valid!")
        else:
            actions = []
            if do_rt: actions.append("RT")
            if do_like: actions.append("Like")
            if do_follow: actions.append("Follow")
            
            selected_accs = sessions[:limit]
            
            with st.status("Sedang menjalankan raid...", expanded=True):
                logs, msg = asyncio.run(raid_process(selected_accs, target_id, actions, min_d, max_d))
                st.dataframe(logs)
                if "RATE LIMIT" in msg: st.error(msg)
                else: st.success("Raid Selesai!")

elif menu == "Scraper Pro":
    st.title("🕵️‍♂️ Scraper Pro (Anti-429)")
    st.info("Kecepatan scraping diperlambat agar tidak terkena Rate Limit.")
    
    col1, col2 = st.columns(2)
    with col1:
        target = st.text_input("Username Target (Tanpa @)")
    with col2:
        mode = st.selectbox("Tipe Data", ["Followers", "Following"])
        limit = st.number_input("Jumlah Ambil", 10, 5000, 50)
        
    if st.button("Ambil Data"):
        with st.spinner("Sedang mengambil data (Sabar, ada delay pengaman)..."):
            data, msg = asyncio.run(scrape_process(target, limit, mode))
            if data:
                st.success(msg)
                st.dataframe(data)
                txt_data = ""
                for d in data:
                    txt_data += f"@{d['Username']} | {d['Umur Akun']} | {d['Joined']}\n"
                st.download_button("Download TXT", txt_data, f"{mode}_{target}.txt")
            else:
                st.error(msg)

elif menu == "Health Checker":
    st.title("🏥 Account Health Checker")
    txt_input = st.text_area("Paste Daftar Username (Pisahkan dengan Enter/Spasi/Koma)", height=200)
    
    if st.button("Cek Kesehatan"):
        if txt_input:
            usernames = list(set(re.findall(r'@?(\w{4,15})', txt_input)))
            usernames = [u for u in usernames if not u.isdigit()]
            
            st.info(f"Mendeteksi {len(usernames)} username unik.")
            
            with st.status("Checking (dengan delay aman)...", expanded=True):
                res = asyncio.run(check_health_process(usernames))
                df = st.dataframe(res)
            
            active = len([x for x in res if x['Status'] == 'ACTIVE'])
            suspend = len([x for x in res if x['Status'] == 'SUSPENDED'])
            st.success(f"Selesai! Active: {active}, Suspended: {suspend}")
        else:
            st.warning("Masukkan username dulu.")

# Footer
st.sidebar.divider()
st.sidebar.caption("Wurk Ultimate Web v4.1 (Safe)")