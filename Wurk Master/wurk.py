import asyncio
import os
import json
import random
import re
import shutil
from datetime import datetime, timezone
from twikit import Client
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import print as rprint
from rich.markup import escape

# --- KONFIGURASI SYSTEM ---
SESSION_DIR = 'sessions'
CONFIG_FILE = 'config.json'
BACKUP_FILE = 'sessions_backup.zip'
console = Console()

# USER AGENT
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

client = Client('en-US', user_agent=USER_AGENT)
CURRENT_USER = None 

if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)

# --- UTILS ---
def load_config():
    default_config = {"min_delay": 10, "max_delay": 20}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return {**default_config, **json.load(f)}
    return default_config

def save_config(data):
    with open(CONFIG_FILE, 'w') as f: json.dump(data, f)

CONFIG = load_config()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def extract_info_from_link(text):
    match_link = re.search(r'(?:x|twitter)\.com/([^/]+)/status/(\d+)', text)
    if match_link: return match_link.group(2), match_link.group(1) 
    match_id = re.search(r'(\d+)', text)
    if match_id and len(match_id.group(1)) > 10: return match_id.group(1), None 
    return None, None

def extract_usernames_strict(text):
    """
    HANYA mengambil kata yang diawali '@'.
    Contoh: 'halo @budi dan tono' -> Hasil: ['budi'] (tono diabaikan)
    """
    # Regex: Cari @ diikuti huruf/angka/garisbawah
    matches = re.findall(r'@(\w{3,25})', text)
    return list(set(matches))

def calculate_account_age(created_at_str):
    try:
        dt_obj = datetime.strptime(created_at_str, '%a %b %d %H:%M:%S %z %Y')
        now = datetime.now(timezone.utc)
        days = (now - dt_obj).days
        if days < 30: return f"[green]{days} Hari[/green]"
        elif days < 365: return f"[yellow]{days // 30} Bulan[/yellow]"
        else: return f"[cyan]{days // 365} Tahun[/cyan]"
    except: return "[dim]-[/dim]"

def show_header():
    clear_screen()
    safe_name = escape(CURRENT_USER['screen_name']) if CURRENT_USER else "[dim red]Offline[/]"
    rprint(Panel.fit(
        f"[bold cyan]WURK ULTIMATE v3.8 (Strict Filter @)[/]\n"
        f"[dim]User:[/dim] {safe_name}",
        border_style="blue"
    ))

# --- ACCOUNT MANAGEMENT ---
async def add_account():
    clear_screen()
    rprint(Panel("Login Manual Cookies", title="Tambah Akun"))
    username_input = Prompt.ask("Username Twitter (Tanpa @)")
    auth = Prompt.ask("auth_token")
    ct0 = Prompt.ask("ct0")
    
    temp_client = Client('en-US', user_agent=USER_AGENT)
    cookies_dict = {"auth_token": auth.strip(), "ct0": ct0.strip()}
    with open('temp.json', 'w') as f: json.dump(cookies_dict, f)
    
    try:
        with Progress(SpinnerColumn(), TextColumn("Verifikasi..."), transient=True) as p:
            p.add_task("", total=None)
            temp_client.load_cookies('temp.json')
            user = await temp_client.get_user_by_screen_name(username_input)
        filename = os.path.join(SESSION_DIR, f"{user.screen_name}.json")
        temp_client.save_cookies(filename)
        rprint(f"[green]✔ Login Sukses: @{escape(user.screen_name)}[/green]")
    except Exception as e: rprint(f"[bold red]Gagal Login![/bold red] {str(e)[:100]}")
    if os.path.exists('temp.json'): os.remove('temp.json')
    Prompt.ask("Enter...")

async def export_sessions():
    if not os.listdir(SESSION_DIR): return rprint("[red]Kosong![/red]")
    try: shutil.make_archive('sessions_backup', 'zip', SESSION_DIR); rprint(f"[green]✔ Backup OK[/green]")
    except Exception as e: rprint(f"[red]Fail: {e}[/red]")
    Prompt.ask("Enter...")

async def import_sessions():
    if not os.path.exists(BACKUP_FILE): return rprint(f"[red]File zip tidak ada![/red]")
    if Confirm.ask("Timpa akun lama?"):
        try: shutil.unpack_archive(BACKUP_FILE, SESSION_DIR); rprint("[green]✔ Restore OK[/green]")
        except: rprint("[red]Fail[/red]")
    Prompt.ask("Enter...")

async def switch_account_menu():
    files = [f for f in os.listdir(SESSION_DIR) if f.endswith('.json')]
    if not files: return rprint("[yellow]No Accounts.[/yellow]")
    rprint("[bold]Pilih Akun:[/bold]")
    for idx, f in enumerate(files, 1): print(f"[{idx}] {f.replace('.json', '')}")
    c = IntPrompt.ask("Nomor", default=1)
    if 1 <= c <= len(files): await load_manual_account(files[c-1].replace('.json', ''))

async def load_manual_account(username):
    global CURRENT_USER
    try:
        client.load_cookies(os.path.join(SESSION_DIR, f"{username}.json"))
        user = await client.get_user_by_screen_name(username)
        CURRENT_USER = {"screen_name": user.screen_name, "id": user.id}
        rprint(f"[green]Aktif: @{escape(username)}[/green]")
        await asyncio.sleep(1)
    except: rprint(f"[red]Gagal Load[/red]")

# --- ANALYST TOOL ---
async def scrape_target():
    clear_screen()
    files = [f for f in os.listdir(SESSION_DIR) if f.endswith('.json')]
    if not files: return rprint("[red]Butuh 1 akun login![/red]")
    
    rprint(Panel("[bold cyan]SCRAPER PRO[/bold cyan]", border_style="cyan"))
    target_username = Prompt.ask("Username Target")
    
    scraper = Client('en-US', user_agent=USER_AGENT)
    try:
        scraper.load_cookies(os.path.join(SESSION_DIR, files[0]))
        with Progress(SpinnerColumn(), TextColumn("Analisa..."), transient=True) as p:
            p.add_task("", total=None)
            target_user = await scraper.get_user_by_screen_name(target_username)
            
        rprint(Panel(f"Target: @{target_user.screen_name}\nFollowers: {target_user.followers_count}\nFollowing: {target_user.following_count}"))
        
        mode = Prompt.ask("Ambil data?", choices=["1 (Followers)", "2 (Following)"], default="1")
        fetch_func = target_user.get_followers if mode.startswith("1") else target_user.get_following
        total_avail = target_user.followers_count if mode.startswith("1") else target_user.following_count
        
        limit = IntPrompt.ask("Jumlah ambil", default=total_avail)
        all_data = []
        
        with Progress(SpinnerColumn(), TextColumn(f"[cyan]Scraping...[/cyan]"), transient=False) as p:
            task = p.add_task("fetch", total=None)
            try:
                batch = await fetch_function(count=40)
                all_data.extend(batch)
                p.update(task, completed=1, description=f"Got: {len(all_data)}")
                while len(all_data) < limit and batch.next_cursor:
                    await asyncio.sleep(1.5)
                    batch = await batch.next()
                    if not batch: break
                    all_data.extend(batch)
                    p.update(task, advance=1, description=f"Got: {len(all_data)}")
            except Exception as e: rprint(f"[yellow]Stop: {e}[/yellow]")

        final_list = all_data[:limit]
        
        table = Table(title=f"Preview Data")
        table.add_column("Username", style="white"); table.add_column("Umur", style="bold"); table.add_column("Join", style="dim")
        for user in final_list[:10]:
            table.add_row(f"@{user.screen_name}", calculate_account_age(user.created_at), str(user.created_at))
        console.print(table)

        file_name = f"{'followers' if mode.startswith('1') else 'following'}_{target_username}.txt"
        if Confirm.ask(f"Simpan ke {file_name}?"):
            with open(file_name, "w", encoding="utf-8") as f:
                for user in final_list:
                    raw_age = calculate_account_age(user.created_at).replace('[green]','').replace('[/green]','').replace('[yellow]','').replace('[/yellow]','').replace('[cyan]','').replace('[/cyan]','')
                    f.write(f"@{user.screen_name} | {raw_age} | {user.created_at}\n")
            rprint("[green]Saved![/green]")
    except Exception as e: rprint(f"[red]Err: {e}[/red]")
    Prompt.ask("Enter...")

# --- HEALTH CHECKER (STRICT FILTER @) ---
async def check_health():
    clear_screen()
    files = [f for f in os.listdir(SESSION_DIR) if f.endswith('.json')]
    if not files: return rprint("[red]Butuh 1 akun login![/red]")
    
    rprint(Panel("[bold red]🏥 ACCOUNT HEALTH CHECKER[/bold red]\n(Hanya mengecek kata yang diawali @)", border_style="red"))
    file_path = Prompt.ask("File TXT Username")
    if not os.path.exists(file_path): return rprint("[red]File 404![/red]") or Prompt.ask("Enter...")
    
    with open(file_path, 'r', encoding='utf-8') as f: content = f.read()
    
    # PANGGIL FUNGSI STRICT FILTER
    usernames = extract_usernames_strict(content)
    
    if not usernames:
        rprint("[bold red]Tidak ditemukan username dengan awalan '@'![/bold red]")
        rprint("Pastikan format di file txt: @username")
        return Prompt.ask("Enter...")

    rprint(f"[cyan]Ditemukan {len(usernames)} username valid (@). Memulai diagnosa...[/cyan]\n")
    
    checker = Client('en-US', user_agent=USER_AGENT)
    checker.load_cookies(os.path.join(SESSION_DIR, files[0]))
    
    table = Table(title="Health Report"); table.add_column("User"); table.add_column("Status"); table.add_column("Info")
    vc, sc, mc = 0, 0, 0
    
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), BarColumn()) as p:
        task = p.add_task("Check", total=len(usernames))
        for uname in usernames:
            p.update(task, description=f"Checking @{uname}")
            try:
                u = await checker.get_user_by_screen_name(uname)
                if u.protected: st="[yellow]LOCKED[/yellow]"; dt="Private"; vc+=1
                else: st="[green]ACTIVE[/green]"; dt=f"{u.followers_count} Fol"; vc+=1
            except Exception as e:
                err = str(e).lower()
                if "suspend" in err: st="[bold red]SUSPEND[/bold red]"; dt="Ban"; sc+=1
                elif "not found" in err or "404" in err: st="[red]MISSING[/red]"; dt="404"; mc+=1
                else: st="[yellow]UNKNOWN[/yellow]"; dt=err[:10]
            table.add_row(f"@{uname}", st, dt)
            p.advance(task)
            await asyncio.sleep(1.5)
            
    console.print(table)
    rprint(f"Active: {vc} | Suspended: {sc} | Missing: {mc}")
    Prompt.ask("Enter...")

# --- WURK ASSISTANT (ON-DEMAND SPEED) ---
async def wurk_assistant():
    clear_screen()
    files = [f for f in os.listdir(SESSION_DIR) if f.endswith('.json')]
    if not files: return rprint("[red]Tidak ada akun![/red]")
    
    rprint(Panel(f"[bold magenta]WURK ASSISTANT[/bold magenta]\nPasukan: {len(files)} Akun", border_style="magenta"))
    
    raw_input = Prompt.ask("Link Tweet Lengkap")
    target_id, target_username = extract_info_from_link(raw_input)
    if not target_id: return rprint("[red]Link Invalid![/red]") or Prompt.ask("Enter...")
    rprint(f"[cyan]Target: {target_id} | @{target_username}[/cyan]")

    rprint("\n[bold]Pilih Template:[/bold]")
    rprint("[1] [cyan]wBasic[/cyan]  (RT)")
    rprint("[2] [yellow]wLike[/yellow]   (RT + Like)")
    rprint("[3] [green]wFollow[/green] (RT + Like + Follow)")
    mode = Prompt.ask("Mode", choices=["1", "2", "3"])
    
    limit = IntPrompt.ask("Jumlah Akun", default=len(files))
    selected_files = files[:limit]

    # --- SPEED SETTING ON ACTION ---
    rprint("\n[bold]Atur Kecepatan Raid:[/bold]")
    rprint("[1] 🐢 Safe (30-60s)")
    rprint("[2] 🚗 Normal (10-20s)")
    rprint("[3] ⚡ Fast (5-10s)")
    rprint("[4] 🚀 Turbo (1-3s)")
    rprint("[5] ⚙  Config Global")
    
    speed_choice = Prompt.ask("Speed", choices=["1","2","3","4","5"], default="2")
    
    if speed_choice == "1": min_d, max_d = 30, 60
    elif speed_choice == "2": min_d, max_d = 10, 20
    elif speed_choice == "3": min_d, max_d = 5, 10
    elif speed_choice == "4": min_d, max_d = 1, 3
    else:
        min_d = CONFIG.get('min_delay', 10)
        max_d = CONFIG.get('max_delay', 20)

    table = Table(title=f"RAID REPORT | {target_id}", show_lines=True)
    table.add_column("User", style="cyan", width=15); table.add_column("RT", width=5); table.add_column("Like", width=5); table.add_column("Follow", width=5)

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), BarColumn()) as p:
        task = p.add_task("[magenta]Raiding...", total=len(selected_files))
        
        for filename in selected_files:
            uname = filename.replace('.json', '')
            fpath = os.path.join(SESSION_DIR, filename)
            st_rt, st_like, st_follow = "[dim]➖[/dim]", "[dim]➖[/dim]", "[dim]➖[/dim]"
            
            p.update(task, description=f"Processing @{uname}")
            worker = Client('en-US', user_agent=USER_AGENT)
            
            try:
                worker.load_cookies(fpath)
                try: await worker.retweet(target_id); st_rt = "[green]✅[/]"
                except: st_rt = "[red]❌[/]"
                if mode in ["2", "3"]:
                    try: await worker.favorite_tweet(target_id); st_like = "[green]✅[/]"
                    except: st_like = "[red]❌[/]"
                if mode == "3":
                    fs = False
                    if target_username:
                        try: u = await worker.get_user_by_screen_name(target_username); await u.follow(); fs=True
                        except: pass
                    if not fs:
                        try: t = await worker.get_tweet_by_id(target_id); await t.user.follow(); fs=True
                        except: pass
                    st_follow = "[green]✅[/]" if fs else "[red]Fail[/]"
                table.add_row(escape(f"@{uname}"), st_rt, st_like, st_follow)
            except: table.add_row(escape(f"@{uname}"), "[red]Err[/]", "[red]Err[/]", "[red]Err[/]")
            
            p.advance(task)
            if filename != selected_files[-1]:
                delay = random.randint(min_d, max_d)
                p.update(task, description=f"Cooldown {delay}s...")
                await asyncio.sleep(delay)
                
    console.print(table)
    Prompt.ask("Selesai. Enter...")

# --- MAIN MENU ---
async def main_menu():
    while True:
        show_header()
        menu = (
            "[bold magenta]--- ⚡ ACTION ---[/bold magenta]\n"
            "[1] Wurk Assistant (Raid)\n"
            "[2] 🕵️‍♂️ Scraper Pro (Follower/Following)\n"
            "[3] 🏥 Cek Kesehatan Akun (@ Only)\n\n"
            "[bold yellow]--- ⚙ MANAGEMENT ---[/bold yellow]\n"
            "[4] Tambah Akun Baru\n"
            "[5] Ganti Akun Manual\n"
            "[6] 📤 Export Sessions\n"
            "[7] 📥 Import Sessions\n"
            "[0] Keluar"
        )
        console.print(Panel(menu, border_style="white"))
        c = Prompt.ask("Pilih", choices=["1","2","3","4","5","6","7","0"])
        
        if c == "1": await wurk_assistant()
        elif c == "2": await scrape_target()
        elif c == "3": await check_health()
        elif c == "4": await add_account()
        elif c == "5": await switch_account_menu()
        elif c == "6": await export_sessions()
        elif c == "7": await import_sessions()
        elif c == "0": rprint("Bye!"); break

if __name__ == "__main__":
    try: asyncio.run(main_menu())
    except KeyboardInterrupt: print("\nStop.")