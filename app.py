import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
import time

# นำเข้าโมดูลที่เราแยกไฟล์ไว้
import config
import database
import pfsense_api

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# ยามเฝ้าประตู (เช็ค Login)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == config.ADMIN_USER and password == config.ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = "❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง!"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    users = database.get_all_users() # เรียกใช้ฟังก์ชันจากไฟล์ database.py
    return render_template('dashboard.html', users=users)

@app.route('/add_user', methods=['POST'])
@login_required
def add_user():
    usr = request.form.get('username')
    pwd = request.form.get('password')
    if usr and pwd:
        database.add_user(usr, pwd)
        pfsense_api.add_captive_user(usr, pwd) # เรียกใช้ฟังก์ชันจากไฟล์ pfsense_api.py
    return redirect(url_for('index'))

@app.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    usr_to_delete = database.get_username(user_id)
    if usr_to_delete:
        database.delete_user(user_id)
        pfsense_api.del_captive_user(usr_to_delete)
    return redirect(url_for('index'))

@app.route('/reboot', methods=['POST'])
@login_required
def reboot():
    # สั่งให้ไฟล์ pfsense_api ทำงาน
    pfsense_api.reboot_router()
    # โยนหน้าที่แสดงผลไปให้ไฟล์ reboot.html จัดการแทน
    return render_template('reboot.html')

# --- ลบของเก่าทิ้ง แล้ววางโค้ดนี้แทนที่ด้านล่างสุดของ app.py ---

last_rx1, last_tx1 = 0, 0
last_rx2, last_tx2 = 0, 0
last_time = 0

@app.route('/api/stats')
@login_required
def api_stats():
    global last_rx1, last_tx1, last_rx2, last_tx2, last_time
    
    # ดึงเวลา Uptime
    uptime = pfsense_api.execute_ssh("uptime | awk -F, '{print $1}' | sed 's/.*up //'")
    if not uptime: uptime = "Online"
    
    # ดึงข้อมูลการวิ่งของเน็ตทั้ง 2 เส้น (em0 = WAN1, em2 = WAN2)
    net_stats1 = pfsense_api.execute_ssh("netstat -ibn | grep -E '^em0' | head -n 1 | awk '{print $8, $11}'")
    net_stats2 = pfsense_api.execute_ssh("netstat -ibn | grep -E '^em2' | head -n 1 | awk '{print $8, $11}'")
    
    rx_mbps1, tx_mbps1 = 0.0, 0.0
    rx_mbps2, tx_mbps2 = 0.0, 0.0
    current_time = time.time()
    
    try:
        # คำนวณ WAN1
        parts1 = net_stats1.split()
        if len(parts1) >= 2:
            curr_rx1, curr_tx1 = int(parts1[0]), int(parts1[1])
            if last_time > 0:
                tdiff = current_time - last_time
                rx_mbps1 = ((curr_rx1 - last_rx1) * 8 / 1000000) / tdiff
                tx_mbps1 = ((curr_tx1 - last_tx1) * 8 / 1000000) / tdiff
            last_rx1, last_tx1 = curr_rx1, curr_tx1
            
        # คำนวณ WAN2
        parts2 = net_stats2.split()
        if len(parts2) >= 2:
            curr_rx2, curr_tx2 = int(parts2[0]), int(parts2[1])
            if last_time > 0:
                tdiff = current_time - last_time
                rx_mbps2 = ((curr_rx2 - last_rx2) * 8 / 1000000) / tdiff
                tx_mbps2 = ((curr_tx2 - last_tx2) * 8 / 1000000) / tdiff
            last_rx2, last_tx2 = curr_rx2, curr_tx2
            
    except Exception as e:
        print("API Error:", e)
        
    last_time = current_time
    
    # ส่งข้อมูลกลับไปให้หน้าเว็บเป็น JSON
    return jsonify({
        "uptime": uptime, 
        "wan1_rx": round(abs(rx_mbps1), 2), "wan1_tx": round(abs(tx_mbps1), 2),
        "wan2_rx": round(abs(rx_mbps2), 2), "wan2_tx": round(abs(tx_mbps2), 2)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)