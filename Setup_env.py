#!/usr/bin/env python3

import subprocess as sp
import json
import os

def module_download():
    print('-----module download now-----', end='\n\n')
    module_lists = [
        'vim',
        'tshark',
        'qemu',
        'brudge-utils',
        'iptables-persistent',
        'tmux',
        'git-core',
        'build-essential',
        'libssl-dev',
        'libncurses5-dev',
        'unzip',
        'gawk',
        'zliblg-dev',
        'subversion',
        'mercurial',
        'python-2.7',
        'python-twisted',
        'python-mysqldb',
        'python-geoip',
        'python-watchdog',
        'vim',
        'jq',
        'traceroute'
        ]

    for module in module_lists:
        p3 = sp.run(['apt', '-y', 'install', module], stdout=sp.PIPE)
        print(p3.stdout.decode('utf-8'))
    print('-----module download finish-----')

def execute_chmod():
    print('-----Give execute permission-----', end='\n\n')
    chmod_list = []

    p1 = sp.run(
        ['ls'], stdout=sp.PIPE, stderr=sp.PIPE)
    p1_list = p1.stdout.decode('utf-8').split('\n')

    # 空要素の削除
    p1_list.remove('')

    for l in p1_list:
        #print('p1_list:{}'.format(l))
        # 実行権限付与するファイルの一覧 -> p1_list
        if '.sh' in l or '.py' in l:
            chmod_list.append(l)
            for c_l in chmod_list:
                if '~' in c_l or 'Setup_env.py' in c_l:
                    chmod_list.remove(c_l)

    # 実行権限を付与するファイルの一覧表示
    for l in chmod_list:
        print(l)

    yn = input('Can I give execute permission to these files?(y/n):')
    if yn == 'Y' or yn == 'y':
        for l in chmod_list:
            sp.run(['chmod', '+x', l])
        print('Execution right granted!!!')
    else:
        print('Please, restart this program.....')
        exit()

def static_network_env():
    print('----- Setting network environments -----', end='\n\n')
    with open('local_static_honeypot_address.json', 'r') as f:

        # load json type
        env = json.load(f)

        for config in env['configs']:
            print('name: {}'.format(config['name']))
            print('address: {}'.format(config['address']))
            print('netmask: {}'.format(config['netmask']))
            print('gateway: {}'.format(config['gateway']))
            print('dns-nameservers: {}'.format(config['dnsnameservers']), end='\n\n')

        print('Please select the network name you want to set up...')

        name = input('your select name: ')
        if name == env['configs'][0]['name']:
            num_env = 0
        elif name == env['configs'][1]['name']:
            num_env = 1
        elif name == env['configs'][2]['name']:
            num_env = 2

        print('name: {}'.format(env['configs'][num_env]['name']))
        print('address: {}'.format(env['configs'][num_env]['address']))
        print('netmask: {}'.format(env['configs'][num_env]['netmask']))
        print('gateway: {}'.format(env['configs'][num_env]['gateway']))
        print('dns-nameservers: {}'.format(env['configs'][num_env]['dnsnameservers']), end='\n\n')

        yn = input('Is this setting really OK?(y/n): ')
        if yn == 'Y' or yn == 'y':

            # set_static_honeypot_address.shを実行
            sp.run(['./set_static_honeypot_address.sh', str(num_env)])
            print('Setting complete!!!')
        else:
            print('Please, restart this program.....')
            exit()

def qemu_setting():
    print('-----Qemu setting start-----', end='\n\n')
    try:
        if os.path.isfile('/etc/qemu-ifup') and os.path.isfile('/etc/qemu-ifdown'):
            if os.path.isfile('qemu-ifup') and os.path.isfile('qemu-ifdown'):
                p1 = sp.run(['mv', '-f', 'qemu-ifup', '/etc/qemu-up'])
                p2 = sp.run(['mv', '-f', 'qemu-ifdown', '/etc/qemu-ifdown'])
            else:
                print('qemu-ifup or qemu-ifdown is not found...')
                exit(1)
        else:
            print("Qemu can't install")
            exit(1)
        print('Qemu setting finished!!!')
    except OSError:
        print('Unexpected Error...')
        exit(1)

def firewall_setting():
    file_name = '/etc/sysctl.conf'
    fire_setting = [
    'net.ipv4.ip_forward = 1',
    'net.ipv6.conf.all.disable_ipv6 = 1',
    'net.ipv6.conf.default.disable_ipv6 = 1',
    'net.ipv6.conf.lo.disable_ipv6 = 1'
    ]
    print('-----Firewall setting start-----', end='\n\n')

    if os.path.isfile('sysctl.conf') == True:
        print('Edit file name: {}'.format(file_name))

        for l in fire_setting:
            print(l)

        yn = input('Can I edit this file?(y/n)')
        if yn == 'Y' or yn == 'y':

            # firewall_setup.shを実行
            sp.run(['./firewall_setup.sh'])
            print('Setting finished!!!')
        else:
            print('Please, restart this program.....')
            exit()
    else:
        print('firewall_setup.sh is not found...')

if __name__ == '__main__':
    module_download()
    execute_chmod()
    static_network_env()
    qemu_setting()
    firewall_setting()
    print('-----Setting honeypot environment finished-----')
