# -*- coding:utf-8 -*-
from guietta import *
from guietta import _, ___
import pickle
from prettytable import PrettyTable
from PIL import Image, ImageDraw, ImageFont
import datetime


def logingui():
    gui = Gui(['账号：', '__user__'],
              ['密码：', PW('upass')],
              [['登入'], ['注册']])
    gui.events([_, _],
               [_, _],
               [login, register])

    # gui = Gui(
    #
    #     ['<center>A big GUI with all of Guietta''s widgets</center>'],
    #     [HSeparator],
    #
    #     ['Label', 'imagelabel.jpeg', L('another label'), VS('slider1')],
    #     [_, ['button'], B('another button'), III],
    #     ['__edit__', E('an edit box'), _, VSeparator],
    #     [Quit, Ok, Cancel, III],
    #     [Yes, No, _, III],
    #     [HS('slider2'), ___, ___, _])
    gui.run()


def error(errormsg):
    gui = Gui(['错误：', 'error'], [['关闭'], _])
    gui.events([_, _], [closegui, _])
    gui.error = errormsg
    gui.run()


def closegui(gui, *args):
    gui.close()


def login(gui, *args):
    name = str(gui.user)
    pwd = str(gui.upass)
    user = []
    user.extend([name, pwd])
    print('[login]登录:')
    print(user)
    print('[login]登录：')
    print(users)
    for u in users:
        if user == u:
            menugui()
            gui.close()
            return 0
    error("账号或密码错误")


def register(gui, *args):
    name = str(gui.user)
    pwd = str(gui.upass)
    user = []
    user.extend([name, pwd])
    users.append(user)
    print('[register]注册:')
    print(user)
    save_info()


def menugui():
    gui = Gui([['输入汽车信息'], ['显示汽车信息'], ['销售汽车']],
              [['修改汽车信息'], ['销售数据'], _])
    gui.events([cars_input_gui, cars_showinfo_gui, cars_sale_gui],
               [cars_changeinfo_gui, sale_cars_info, _])
    gui.run()


def check_cars(new_car_num):
    for car in cars:
        if new_car_num == car["number"]:
            return False
    return True


def cars_input_gui(gui, *args):
    gui = Gui(['汽车信息录入：', _, _, _],
              ['汽车编号：', '__number__', '汽车名称：', '__name__'],
              ['汽车品牌：', '__brand__', '汽车价格：', '__price__'],
              [['录入'], '', ['取消'], ''])
    gui.events([_, _, _, _],
               [_, _, _, _],
               [_, _, _, _],
               [cars_input_add, _, closegui, _])
    gui.run()


def cars_input_add(gui, *args):
    car = {}
    car["number"] = str(gui.number)
    car["name"] = str(gui.name)
    car["brand"] = str(gui.brand)
    car["price"] = str(gui.price)
    print(car)
    if check_cars(str(gui.number)):
        cars.append(car)
        save_info()
    else:
        error("输入信息存在问题，请检查")


def save_info():
    f1 = open("cars.txt", "wb")
    pickle.dump(cars, f1)
    f1.close()
    f2 = open("users.txt", "wb")
    pickle.dump(users, f2)
    f2.close()
    f3 = open("scars.txt", "wb")
    pickle.dump(scars, f3)
    f3.close()


def update_scars_picture():
    tab = PrettyTable()
    tab.field_names = ["汽车编号", "汽车名称", "汽车品牌", "汽车价格", "销售时间"]
    for scar in scars:
        r = [scar['number'], scar['name'], scar['brand'], scar['price'], scar['time']]
        tab.add_row(r)
    tab_info = str(tab)
    space = 5
    print(tab_info)
    now_time = datetime.datetime.now()
    time1_str = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    tab_info = tab_info + "\n更新时间：" + time1_str
    # PIL模块中，确定写入到图片中的文本字体
    # ubuntu
    # font = ImageFont.truetype('/home/doge/YaHeiConsolas.ttf', 15, encoding='utf-8')
    # windows
    font = ImageFont.truetype('C:\\WINDOWS\\Fonts\\simsun.ttc', 15, encoding="utf-8")
    # Image模块创建一个图片对象
    im = Image.new('RGB', (10, 10), (0, 0, 0, 0))
    # ImageDraw向图片中进行操作，写入文字或者插入线条都可以
    draw = ImageDraw.Draw(im, "RGB")
    # 根据插入图片中的文字内容和字体信息，来确定图片的最终大小
    img_size = draw.multiline_textsize(tab_info, font=font)
    # 图片初始化的大小为10-10，现在根据图片内容要重新设置图片的大小
    im_new = im.resize((img_size[0] + space * 2, img_size[1] + space * 2))
    del draw
    del im
    draw = ImageDraw.Draw(im_new, 'RGB')
    # 批量写入到图片中，这里的multiline_text会自动识别换行符
    # python2
    # draw.multiline_text((space,space), unicode(tab_info, 'utf-8'), fill=(255,255,255), font=font)
    # python3
    draw.multiline_text((space, space), tab_info, fill=(255, 255, 255), font=font)

    im_new.save('scars.PNG', "PNG")
    del draw


def update_cars_picture():
    tab = PrettyTable()
    tab.field_names = ["汽车编号", "汽车名称", "汽车品牌", "汽车价格"]
    for car in cars:
        r = [car['number'], car['name'], car['brand'], car['price']]
        tab.add_row(r)
    tab_info = str(tab)
    space = 5
    print(tab_info)
    now_time = datetime.datetime.now()
    time1_str = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    tab_info = tab_info + "\n更新时间：" + time1_str
    # PIL模块中，确定写入到图片中的文本字体
    # ubuntu
    # font = ImageFont.truetype('/home/doge/YaHeiConsolas.ttf', 15, encoding='utf-8')
    # windows
    font = ImageFont.truetype('C:\\WINDOWS\\Fonts\\simsun.ttc', 15, encoding="utf-8")
    # Image模块创建一个图片对象
    im = Image.new('RGB', (10, 10), (0, 0, 0, 0))
    # ImageDraw向图片中进行操作，写入文字或者插入线条都可以
    draw = ImageDraw.Draw(im, "RGB")
    # 根据插入图片中的文字内容和字体信息，来确定图片的最终大小
    img_size = draw.multiline_textsize(tab_info, font=font)
    # 图片初始化的大小为10-10，现在根据图片内容要重新设置图片的大小
    im_new = im.resize((img_size[0] + space * 2, img_size[1] + space * 2))
    del draw
    del im
    draw = ImageDraw.Draw(im_new, 'RGB')
    # 批量写入到图片中，这里的multiline_text会自动识别换行符
    # python2
    # draw.multiline_text((space,space), unicode(tab_info, 'utf-8'), fill=(255,255,255), font=font)
    # python3
    draw.multiline_text((space, space), tab_info, fill=(255, 255, 255), font=font)

    im_new.save('cars.PNG', "PNG")
    del draw


def cars_showinfo_gui(gui, *args):
    # guis = []
    # for car in cars:
    #     g = []
    #     g.append('汽车编号：')
    #     g.append(car['number'])
    #
    #     #g = ['汽车编号：', car['number'], '汽车名称:', car['name'], '汽车品牌:', car['brand'], '汽车价格:', car['price']]
    #     guis.append(g)
    # lastline = []
    # lastline.append('Close')
    # lastline.append(_)
    # # for i in range(6):
    # #     lastline.append(_)
    # # guis.append([,_,_,_,_,_,_,_])
    # guis.append(lastline)
    # print(",".join('%s' %id for id in guis))
    #
    # gui = Gui(",".join('%s' %id for id in guis))
    # with gui.Close:
    #     closegui()
    update_cars_picture()
    gui = Gui(['cars.png'])
    gui.run()


def cars_sale_gui(gui,*args):
    # guis = []
    # guis.append('<center>查看汽车列表</center>')
    # guis.append([HSeparator])
    # for car in cars:
    #     g = []
    #     # g.append('汽车编号：')
    #     # g.append(car['number'])
    #     g = ['汽车编号：', car['number'], '汽车名称:', car['name'], '汽车品牌:', car['brand'], '汽车价格:', car['price']]
    #
    #     guis.append(g)
    # guis.append([HSeparator])
    # guis.append(['输入销售的汽车编号：', '__number__', _, _, _, _, _, _])
    # guis.append([['销售'], ['关闭'], _, _, _, _, _, _])
    # gui = Gui(guis)
    # with guis.关闭:
    #     closegui()
    # with guis.销售:
    #     for car in cars:
    #         if guis.number == car.get("number"):
    #             f = open("sale.txt", "a+")
    #             f.write("\t汽车编号：" + str(car["number"]) + \
    #                     "\t汽车名：" + str(car["name"]) + \
    #                     "\t品牌：" + str(car["brand"]) + \
    #                     "\t价格：" + str(car["price"]) + "\n")
    #             f.close()
    #             cars.remove(car)
    #     save_info()
    #     gui.close()
    #     cars_sale_gui()
    update_cars_picture()
    update_scars_picture()
    gui = Gui(['<center>汽车列表</center>'], ['cars.png'], [HSeparator], ['<center>已销售汽车列表</center>'], ['scars.png'],
              [HSeparator], ['输入序号：', '__num__'], [['销售']])
    gui.events([_], [_], [_], [_], [_],
              [_], [_, _], [cars_sale_sale])
    gui.run()

def cars_sale_sale(gui,*args):
    print("[ cars_sale_sale]调用")
    update_cars_picture()
    update_scars_picture()
    for car in cars:
        if gui.num == car.get("number"):
            print("[ cars_sale_sale]遍历")
            print(car.get("number"))
            scar = car
            now_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
            scar["time"] = time_str
            scars.append(scar)
            cars.remove(car)
            print("[ cars_sale_sale]scars")
            print(scars)
            save_info()

def cars_changeinfo_gui(gui,*args):
    update_cars_picture()
    gui = Gui(['<center>修改汽车信息</center>'],[HSeparator],['cars.png'],[HSeparator],['输入序号:','__num__'],[['修改']])
    gui.events([_],[_],[_],[_],[_,_],[cars_changeinfo_changegui])
    gui.run()

def cars_changeinfo_changegui(gui,*args):
    for car in cars:
        if gui.num == car.get("number"):
            g = Gui(['车辆编号:','__number__','原编号:',car['number']],
                    ['车辆名称','__name__','原名称:',car['name']],
                    ['车辆品牌','__brand__','原品牌:',car['brand']],
                    ['车辆价格','__price__','原价格:',car['price']],
                    [['修改']])
            g.events([_,_,_,_],
                    [_,_,_,_],
                    [_,_,_,_],
                    [_,_,_,_],
                    [cars_changeinfo_change])
            g.run()
            cars.remove(car)

def cars_changeinfo_change(gui,*args):
    car = {}
    car["number"] = str(gui.number)
    car["name"] = str(gui.name)
    car["brand"] = str(gui.brand)
    car["price"] = str(gui.price)
    print(car)
    if check_cars(str(gui.number)):
        cars.append(car)
        save_info()
        gui.close()
    else:
        error("输入信息存在问题，请检查")


def cars_init():
    cars = []
    carsinfo = open("cars.txt", "rb+")
    try:
        cars = pickle.load(carsinfo)
    except EOFError:
        return cars
    return cars

def sale_cars_info(gui,*args):
    update_scars_picture()
    gui = Gui(['scars.png'])
    gui.run()


def users_init():
    users = []
    f = open("users.txt", "rb+")
    try:
        users = pickle.load(f)
    except EOFError:
        return users
    return users


def scars_init():
    scars = []
    f = open("scars.txt", "rb+")
    try:
        scars = pickle.load(f)
    except EOFError:
        return scars
    return scars


cars = cars_init()
users = users_init()
scars = scars_init()
logingui()
