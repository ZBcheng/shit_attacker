<template>
    <form class="col s12" method="POST" @submit.prevent="startAttack" id="ip_form">
        <div id="index">

            <div v-if="this.render_card == 'pass_card'">
                <div class="row" id="pass_card" style="margin-top: 15%;">
                    <div class="card" style="width: 50%; margin-left: 25%; margin-top: 10%">
                        <div class="card-content">
                            <h4 style="margin-top: 3%">本机密码</h4>
                            <div class="input-field">
                                <input type="password" id="localpass-input" class="autocomplete" style="width: 50%">
                            </div>
                            <div>
                                <a class="btn deep-purple accent-3" @click="setPass()"
                                    style="width:50%; margin-top: 3%; margin-bottom: 3%;">CONFIRM</a>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
            <div v-else-if="this.render_card == 'ip_info_card'">
                <nav>
                    <div class="nav-wrapper deep-purple accent-3">
                        <div class="input-field">
                            <input id="search" type="search" required>
                            <label class="label-icon" for="search"><i class="material-icons">search</i></label>
                            <i class="material-icons">close</i>
                        </div>
                    </div>
                </nav>

                <div class="row" style="margin-top: 5%;">
                    <div class="col s1"></div>
                    <div class="col s3">
                        <div class="card">
                            <div class="card-content">
                                <span class="card-title">攻击IP列表</span>
                                <h5 v-for="ip in this.selected_ip" :key="ip">
                                    {{ ip }}
                                </h5>
                            </div>
                            <div class="card-action">
                                <a class="btn modal-trigger deep-purple accent-3" href="#modal1"
                                    style="color: white;">开始攻击</a>
                            </div>
                        </div>
                    </div>
                    <div class="col s1"></div>
                    <div class="col s6">
                        <ul id="info_table" class="collapsible">
                            <table class="striped centered highlight" style="font-weight:bold;">
                                <thead>
                                    <tr>
                                        <th style="color: #651fff">选择</th>
                                        <th style="color: #651fff">ip</th>
                                        <th style="color: #651fff">mac</th>
                                        <th style="color: #651fff">详细信息</th>
                                    </tr>
                                </thead>

                                <tbody>
                                    <tr v-for="item in ip_list" :key="item">
                                        <td>
                                            <p>
                                                <label>
                                                    <input type="checkbox" @click="addIP(item.ip)" />
                                                    <span></span>
                                                </label>
                                            </p>
                                        </td>
                                        <td>{{ item.ip }}</td>
                                        <td>{{ item.mac }}</td>
                                        <td>详细信息</td>
                                    </tr>
                                </tbody>
                            </table>
                        </ul>
                    </div>
                </div>



                <input id="ip_input" name="target_ip" value="" hidden>
            </div>
            <div v-else-if="this.render_card == 'attack_card'">
                <div class="row" id="attack_card" style="margin-top: 15%;">
                    <div class="card" style="width: 50%; margin-left: 25%; margin-top: 10%">
                        <div class="card-content">
                            <h4 style="margin-top: 3%">攻击警告⚠️</h4>
                            <h5>正在攻击💣 {{ this.selected_ip }}</h5>
                            <a class="btn modal-trigger deep-purple accent-3" @click="stopAttack()"
                                style="color: white; margin-top: 3%; margin-bottom: 3%;">停止攻击</a>
                        </div>
                    </div>

                </div>
            </div>
        </div>




        <!-- Modal Structure -->
        <div id="modal1" class="modal">
            <div class="modal-content">
                <h4>攻击警告⚠️</h4>
                <h5>{{ this.selected_ip }}</h5>
                <div class="row">
                    <div class="col s12">
                        <div class="input-field inline">
                            <input id="attack_time" name="attack_time" type="text" class="validate">
                            <label for="attack_time">攻击时间(s)</label>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-footer" @click="startAttack()">
                <a class="modal-close waves-effect waves-green btn-flat" onclick="this.startAttack">开始攻击</a>
            </div>
        </div>

        <div id="info_modal" class="modal">
            <div class="modal-content">
                <h4>{{ this.modal_content }}</h4>
            </div>
        </div>
    </form>
</template>

<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
<script src="https://code.jquery.com/jquery-2.1.1.min.js"></script>

<script>
    import axios from 'axios'
    export default {
        name: 'Index',
        data() {
            return {
                render_card: '',
                ip_list: [], // ip列表
                instance: null, // 信息modal
                search_status: '', // IP列表获取状态
                selected_ip: [], // 以选择的ip
                modal_content: '', // 信息modal显示信息
                attack_time: 0, // 攻击时间⌚️
            };
        },
        mounted: function () {
            M.AutoInit()
            this.render_card = "pass_card"
            var elem = document.getElementById('info_modal')
            this.instance = M.Modal.init(elem)
            // var info_table = document.getElementById("info_table")
            // info_table.style.visibility = "hidden"
        },
        methods: {
            close_info_modal() {
                this.instance.close()
            },
            show_info_modal(info) {
                this.modal_content = info
                this.instance.open()
            },
            setPass() {
                this.local_pass = document.getElementById('localpass-input').value
                if (this.local_pass == "") {
                    this.show_info_modal("❌ 密码不能为空")
                } else {
                    axios.post("http://127.0.0.1:5000/setpass/", {
                        headers: {
                            "Access-Control-Allow-Credentials": true,
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Methods": "POST",
                            "Access-Control-Allow-Headers": "Content-Type",
                        },
                        data: {
                            "local_pass": this.local_pass
                        },

                    })
                        .then(response => {
                            var elem = document.getElementById('info_modal')
                            var instances = M.Modal.init(elem)
                            if (response.data == "password set done!") {
                                this.render_card = "ip_info_card"
                                if (this.search_status != "done") {
                                    this.ip_list = this.getIPs()
                                    this.show_info_modal("💻 正在扫描ip....")
                                }
                            } else {
                                this.show_info_modal("🙅‍ 密码错误")
                            }

                        })
                        .catch(response => {
                            this.show_info_modal("response")
                        })
                }
            },
            getIPs() {
                var path = 'http://127.0.0.1:5000/'
                axios.get(path, {
                    headers: {
                        "Access-Control-Allow-Credentials": true,
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "GET",
                        "Access-Control-Allow-Headers": "Content-Type",
                    }
                })
                    .then(response => {
                        this.ip_list = response.data
                        this.search_status = "done"
                        // alert("done")
                        this.close_info_modal()
                    })
                    .catch(response => {
                        return response.data
                    })
            },
            addIP(value) {
                if (this.selected_ip.indexOf(value) <= -1) {
                    this.selected_ip.push(value)
                } else {
                    var index = this.selected_ip.indexOf(value)
                    this.selected_ip.splice(index, 1)
                }
            },
            submitIP(value) {
                this.selected_ip += value + " "
                // var ip_input = document.getElementById('ip_input')
                // ip_input.value = this.selected_ip
            },
            startAttack() {
                var path = 'http://127.0.0.1:5000/arpattack/'
                this.attack_time = document.getElementById('attack_time').value
                var elem = document.getElementById('info_modal')
                var instances = M.Modal.init(elem)
                if (this.attack_time == "") {
                    this.modal_content = "请输入攻击时间⌚️"
                    instances.open()
                } else {
                    // this.modal_content = "正在攻击💣.... " + this.selected_ip
                    this.render_card = "attack_card"
                    // instances.open()
                    axios.post(path, {
                        headers: {
                            "Access-Control-Allow-Credentials": true,
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Methods": "POST",
                            "Access-Control-Allow-Headers": "Content-Type",
                        },
                        data: {
                            "target_ip": this.selected_ip,
                            "attack_time": this.attack_time,
                        },

                    })
                        .then(response => {
                            this.modal_content = this.selected_ip + " 攻击结束"
                            this.render_card = "ip_info_card"
                            this.selected_ip = []
                            var elem = document.getElementById('info_modal')
                            var instance = M.Modal.getInstance(elem);
                            instance.open()
                        })
                        .catch(response => {
                            alert(response.data)
                        })
                }

            },
            stopAttack() {
                var path = 'http://127.0.0.1:5000/stopattack/'
                axios.get(path, {
                    headers: {
                        "Access-Control-Allow-Credentials": true,
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "GET",
                        "Access-Control-Allow-Headers": "Content-Type",
                    }
                })
                    .then(response => {
                        this.selected_ip = []
                        this.render_card = "ip_info_card"
                    })
                    .catch(response => {
                        return response.data
                    })
            },
        }
    }
</script>