# ⚡ SmartNet Gateway (Dual-WAN Edition)

Automated Network Management System & Dashboard for pfSense Router. 
โปรเจคนี้คือระบบศูนย์กลางสำหรับบริหารจัดการเครือข่ายหอพัก/สำนักงาน ที่ผสานการทำงานระหว่าง Network Infrastructure และ Software Engineering เข้าด้วยกัน

## 🌟 Core Features (ความสามารถหลัก)
- **Dual-WAN Load Balancing & Failover:** รองรับการรวมความเร็วอินเทอร์เน็ต 2 เส้น และสลับสายอัตโนมัติเมื่อเน็ตล่ม
- **Real-time Network Telemetry:** แสดงกราฟ Bandwidth Traffic (Rx/Tx) ของทั้ง WAN1 และ WAN2 แบบวินาทีต่อวินาที ผ่านการดึงข้อมูลด้วย SSH Protocol
- **Auto-Provisioning System:** ระบบเพิ่ม/ลบ ผู้ใช้งาน Captive Portal อัตโนมัติ โดย Python จะส่งสคริปต์ไปรันบน pfSense โดยตรง (ไม่ต้องตั้งค่าผ่านหน้าเว็บ Router)
- **Microservices Architecture:** แยกฐานข้อมูลผู้ใช้งาน (Database) ไปรันบน Docker Container (MySQL) เพื่อความเสถียรและย้ายระบบได้ง่าย
- **Remote Execution & Access:** รองรับการสั่ง Reboot Router ผ่าน Web Dashboard และสามารถเชื่อมต่อจากภายนอกด้วย ngrok (Cloudflare Tunnel alternative)

## 🛠️ Technology Stack
- **Infrastructure:** pfSense (FreeBSD), VMware
- **Backend:** Python (Flask, Paramiko SSH, PyMySQL)
- **Database:** MySQL 8.0 (Docker Container)
- **Frontend:** HTML5, CSS3, JavaScript (Chart.js)
- **Networking:** TCP/IP, SSH (Port 22), Load Balance, Captive Portal

## 🚀 How to Run (วิธีใช้งานเบื้องต้น)
1. Start MySQL Database: `docker start smartnet-db`
2. Run Web Dashboard: `python app.py`
3. Access via Browser: `http://127.0.0.1:5000`
