import random
import sys
import libvirt
import xml.dom.minidom as minidom
from uuid import uuid4


def init():
    global conn
    conn = libvirt.open('qemu:///system')
    if conn is None:
        print('无法连接至 qemu:///system', file=sys.stderr)
        exit(1)


def link(domName):
    dom = conn.lookupByName(domName)
    if dom is None:
        print('无法找到Domain:' + domName, file=sys.stderr)
        exit(1)
    name = dom.hostname()
    print('The hostname of the domain is ' + str(name))


# virDomainState
def getDomainStateStr(domainstate: int):
    domainStateStr = ['无状态', '运行中', '被阻止', '暂停', '正在关闭', '关闭', '崩溃', '被访客电源管理暂停', '最后状态']
    return domainStateStr[domainstate]


def listDomains():
    # defined_domains = conn.listDefinedDomains()
    domain_list = conn.listAllDomains()
    # print(domain_list)
    # print(defined_domains)
    # domains_stats = conn.vi
    for domain in domain_list:
        domain_stat = domain.state()[0]
        if (domain_stat == 1):
            domain_is_running = True
        else:
            domain_is_running = False
        print("------" + str(domain.name()) + ':' + getDomainStateStr(domain_stat) + "------")
        print('虚拟机名称:' + str(domain.name()))
        if (domain_is_running):
            print("虚拟机ID：" + str(domain.ID()))
            print("虚拟机当前状态:" + getDomainStateStr(domain_stat))
            domain_memory_state = domain.memoryStats();
            print('虚拟机内存：  ' + ' 最大内存:' + str(domain.maxMemory() / 1024) + 'MB')
            # print(domain_memory_state)
            # print('可用内存:'+str(domain_memory_state['available']/1024))
            print('虚拟机CPU核数：' + str(domain.maxVcpus()))

        # print
        # "虚拟机信息: {}".format(domain.info())
        # print
        # "虚拟机最大内存:{} MB".format((domain.maxMemory() / 1024))
        # print
        # "虚拟机内存状态:{}".format(domain.memoryStats())
        # print
        # "虚拟机CPU核数:{}".format(domain.maxVcpus())
        # print(info)


# def temp(name: str):
#     f = open('/etc/libvirt/qemu/{}.xml'.format(name))  # xml文件需要事先准备好
#     xml = f.read()
#     conn.createXML(xml)
#     f.close()
#     print("临时虚拟机 {} 创建".format(name))


def define(name: str):

    if name == '¿':
        name = input('请输入要操作的虚拟机名称：')
    xml_path = '/etc/libvirt/qemu/{}.xml'.format(name)
    try:
        if input_default('是否从img文件安装？【默认值y】','y')=='y':

            create_xml(xml_path,True,name)
            f = open(xml_path)
            xml = f.read()
            dom = conn.defineXML(xml)
            f.close()
        else:
            xmldesc = '<volume type="file"><name>{}.qcow2</name><allocation unit="M">10</allocation><capacity ' \
                      'unit="M">1000</capacity><target><path>/var/lib/libvirt/images/{}.qcow2</path><format ' \
                      'type="qcow2"/></target></volume>'.format(name, name)
            storage_pool = conn.storagePoolLookupByName('default')
            storage_vol = storage_pool.createXML(xmldesc, 0)
            storage_vol_info = storage_vol.info()
            create_xml(xml_path,False,name)
            f = open(xml_path)  # xml文件需要事先准备好
            xml = f.read()
            dom = conn.defineXML(xml)
            f.close()

    except libvirt.libvirtError:
        print("[libvirtError]错误：虚拟机操作错误，请检查错误语句\n请注意虚拟机的打开与关闭状态以及是否拼写正确虚拟机的名称")
        return 1
    except:
        print("未预料的错误:", sys.exc_info()[0])
        raise
        return 1

    print("虚拟机 {} 创建".format(name))


def undefine(name: str):
    if name == '¿':
        name = input('请输入要操作的虚拟机名称：')
    try:
        dom = conn.lookupByName(name)
        dom.undefine()
    except libvirt.libvirtError:
        print("[libvirtError]错误：虚拟机操作错误，请检查错误语句\n请注意虚拟机的打开与关闭状态以及是否拼写正确虚拟机的名称")
        return 1
    except:
        print("未预料的错误:", sys.exc_info()[0])
        raise
        return 1

    print("虚拟机 {} 已取消定义".format(name))


def suspend(name: str):
    if name == '¿':
        name = input('请输入要操作的虚拟机名称：')
    try:
        dom = conn.lookupByName(name)
        dom.suspend()
    except libvirt.libvirtError:
        print("[libvirtError]错误：虚拟机操作错误，请检查错误语句\n请注意虚拟机的打开与关闭状态以及是否拼写正确虚拟机的名称")
        return 1
    except:
        print("未预料的错误:", sys.exc_info()[0])
        raise
        return 1

    print("虚拟机 {} 暂停".format(name))


def resume(name: str):
    if name == '¿':
        name = input('请输入要操作的虚拟机名称：')
    try:
        dom = conn.lookupByName(name)
        dom.resume()
    except libvirt.libvirtError:
        print("[libvirtError]错误：虚拟机操作错误，请检查错误语句\n请注意虚拟机的打开与关闭状态以及是否拼写正确虚拟机的名称")
        return 1
    except:
        print("未预料的错误:", sys.exc_info()[0])
        raise
        return 1

    print("虚拟机 {} 运行".format(name))


def destroy(name: str):
    if name == '¿':
        name = input('请输入要操作的虚拟机名称：')
    try:
        dom = conn.lookupByName(name)
        dom.destroy()
    except libvirt.libvirtError:
        print("[libvirtError]错误：虚拟机操作错误，请检查错误语句\n请注意虚拟机的打开与关闭状态以及是否拼写正确虚拟机的名称")
        return 1
    except:
        print("未预料的错误:", sys.exc_info()[0])
        raise
        return 1

    print("虚拟机 {} 销毁".format(name))


def start(name: str):
    if name == '¿':
        name = input('请输入要操作的虚拟机名称：')
    try:
        dom = conn.lookupByName(name)
        dom.create()
    except libvirt.libvirtError:
        print("[libvirtError]错误：虚拟机操作错误，请检查错误语句\n请注意虚拟机的打开与关闭状态以及是否拼写正确虚拟机的名称")
        return 1
    except:
        print("未预料的错误:", sys.exc_info()[0])
        raise
        return 1

    print("虚拟机 {} 启动".format(name))


def shutdown(name: str):
    if name == '¿':
        name = input('请输入要操作的虚拟机名称：')
    try:
        dom = conn.lookupByName(name)
        dom.shutdown()
    except libvirt.libvirtError:
        print("[libvirtError]错误：虚拟机操作错误，请检查错误语句\n请注意虚拟机的打开与关闭状态以及是否拼写正确虚拟机的名称")
        return 1
    except:
        print("未预料的错误:", sys.exc_info()[0])
        raise
        return 1

    print("虚拟机 {} 关闭成功".format(name))




def input_default(prompt: str, defaultvalue: str):
    result = input(prompt)
    if result.strip() == '':
        result = defaultvalue
    return result


def randomMAC():
    mac = [0x52, 0x54, 0x00,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def create_xml(xml_path:str,img:bool,name_of_target:str):
    print('现在开始进行虚拟机设置：')
    print(img)
    dom = minidom.getDOMImplementation().createDocument(None, 'domain', None)
    domain = dom.documentElement  # 虚拟机
    domain.setAttribute('type', 'kvm')

    name = dom.createElement('name')  # 虚拟机名称
    name.appendChild(dom.createTextNode(input_default('请输入虚拟机名称：', 'EmptyName')))
    domain.appendChild(name)

    uuid = dom.createElement('uuid')  # 虚拟机uuid
    uuid.appendChild(dom.createTextNode(str(uuid4())))
    domain.appendChild(uuid)

    memory = dom.createElement('memory')  # 虚拟机内存
    memory.setAttribute('unit', 'MiB')
    memory.appendChild(dom.createTextNode(input_default('请输入虚拟机内存【单位：MB，默认值512】：', '512')))
    domain.appendChild(memory)

    # currentMemory = dom.createElement('currentMemory')
    vcpu = dom.createElement('vcpu')
    vcpu.appendChild(dom.createTextNode(input_default('请输入虚拟机vcpu数量【默认值1】：', '1')))
    domain.appendChild(vcpu)

    os = dom.createElement('os')
    type = dom.createElement('type')
    type.setAttribute('arch', 'x86_64')
    type.setAttribute('machine', 'pc')
    type.appendChild(dom.createTextNode('hvm'))
    boot = dom.createElement('boot')
    if img:
        boot.setAttribute('dev', 'hd')
    else:
        boot.setAttribute('dev', 'cdrom')
    os.appendChild(type)
    os.appendChild(boot)
    domain.appendChild(os)

    features = dom.createElement('features')
    acpi = dom.createElement('acpi')
    apic = dom.createElement('apic')
    features.appendChild(acpi)
    features.appendChild(apic)
    domain.appendChild(features)

    clock = dom.createElement('clock')
    clock.setAttribute('offset', 'localtime')
    domain.appendChild(clock)

    on_poweroff = dom.createElement('on_poweroff')
    on_poweroff.appendChild(dom.createTextNode('destroy'))
    on_reboot = dom.createElement('on_reboot')
    on_reboot.appendChild(dom.createTextNode('restart'))
    on_crash = dom.createElement('on_crash')
    on_crash.appendChild(dom.createTextNode('restart'))
    domain.appendChild(on_poweroff)
    domain.appendChild(on_reboot)
    domain.appendChild(on_crash)

    devices = dom.createElement('devices')

    emulator = dom.createElement('emulator')
    emulator.appendChild(
        dom.createTextNode(input_default('请输入模拟器所在路径【默认值：/usr/bin/qemu-system-x86_64】', '/usr/bin/qemu-system-x86_64')))
    devices.appendChild(emulator)

    disk = dom.createElement('disk')
    disk.setAttribute('type', 'file')
    disk.setAttribute('device', 'disk')
    driver = dom.createElement('driver')
    driver.setAttribute('name', 'qemu')
    driver.setAttribute('type', input_default('请输入镜像文件类型【默认值qcow2】', 'qcow2'))
    disk.appendChild(driver)
    source = dom.createElement('source')
    img_path = ''
    if not img:
        img_path = '/var/lib/libvirt/images/{}.qcow2'.format(name_of_target)
    print(img_path)
    while img_path.strip() == '':
        img_path = input('请输入镜像文件位置')
    source.setAttribute('file', img_path)
    disk.appendChild(source)
    target = dom.createElement('target')
    target.setAttribute('dev', 'hda')
    target.setAttribute('bus', 'ide')
    disk.appendChild(target)
    devices.appendChild(disk)
    if not img:
        disk_cdrom = dom.createElement('disk')
        disk_cdrom.setAttribute('type', 'file')
        disk_cdrom.setAttribute('device', 'cdrom')
        source_cdrom = dom.createElement('source')
        iso_path = ''
        while iso_path.strip()=='':
            iso_path = input('请输入iso文件位置')
        source_cdrom.setAttribute('file', iso_path)
        target_cdrom = dom.createElement('target')
        target_cdrom.setAttribute('dev', 'hdb')
        target_cdrom.setAttribute('bus', 'ide')
        disk_cdrom.appendChild(source_cdrom)
        disk_cdrom.appendChild(target_cdrom)
        devices.appendChild(disk_cdrom)

    interface = dom.createElement('interface')
    interfacetype = input_default('请输入网络配置类型【默认值network】', 'network')
    interface.setAttribute('type',interfacetype)
    mac = dom.createElement('mac')
    mac.setAttribute('address', randomMAC())
    interface.appendChild(mac)
    source_i = dom.createElement('source')
    if interfacetype=='network':
        #network
        source_i.setAttribute('network','default')
    elif interfacetype=='bridge':
        #bridge
        source_i.setAttribute('bridge', 'br0')
    interface.appendChild(source_i)
    devices.appendChild(interface)

    input_keyboard = dom.createElement('input')
    input_mouse = dom.createElement('input')
    input_keyboard.setAttribute('type','keyboard')
    input_mouse.setAttribute('type', 'mouse')
    input_keyboard.setAttribute('bus', 'ps2')
    input_mouse.setAttribute('bus', 'ps2')
    devices.appendChild(input_keyboard)
    devices.appendChild(input_mouse)

    graphics = dom.createElement('graphics')
    graphics.setAttribute('type','vnc')
    graphics.setAttribute('autoport', 'yes')
    graphics.setAttribute('keymap', 'en-us')
    graphics.setAttribute('listen', '0.0.0.0')
    devices.appendChild(graphics)

    memballoon = dom.createElement('memballoon')
    memballoon.setAttribute('model','virtio')
    stats = dom.createElement('stats')
    stats.setAttribute('period','10')
    memballoon.appendChild(stats)
    devices.appendChild(memballoon)

    domain.appendChild(devices)





    try:
        with open(xml_path, 'w', encoding='UTF-8') as fh:
            # dom.writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
            # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
            dom.writexml(fh, indent='', addindent='', newl='', encoding='UTF-8')
            print('写入xml OK!')
    except Exception as err:
        print('错误信息：{0}'.format(err))

def helpinfo():
    print("------ 帮助 ------")
    print('help/h：显示本帮助信息')
    print('quit/q：退出')
    print('start/s [名称]：启动')
    print('destroy/d [名称]：销毁')
    print('shutdown/st [名称]：关闭')
    print('suspend/su [名称]：暂停')
    print('resume/r [名称]：恢复')
    print('create/cr [名称]：创建')
    print('delete/de [名称]：删除')

def menu():
    while True:
        inputcmd = input(">")
        cmd = inputcmd.split()
        if len(cmd) == 1:
            cmdp = False
            cmd.append("¿")
        else:
            cmdp = True
        if cmd[0] == "list" or cmd[0] == "l":
            listDomains()
        elif cmd[0] == "quit" or cmd[0] == "q":
            exit(0)
        elif cmd[0] == "start" or cmd[0] == "s":
            start(cmd[1])
        elif cmd[0] == "destroy" or cmd[0] == "d":
            destroy(cmd[1])
        elif cmd[0] == "shutdown" or cmd[0] == "st":
            shutdown(cmd[1])
        elif cmd[0] == "resume" or cmd[0] == "r":
            resume(cmd[1])
        elif cmd[0] == "create" or cmd[0] == "cr":
            define(cmd[1])
        elif cmd[0] == "delete" or cmd[0] == "de":
            undefine(cmd[1])
        elif cmd[0] == "suspend" or cmd[0] == "su":
            suspend(cmd[1])
        elif cmd[0] == "help" or cmd[0] == "h":
            helpinfo()


        else:
            print("指令错误，请检查输入指令")


init()
menu()
