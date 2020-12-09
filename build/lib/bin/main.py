from persontax.verification import VerificationCollection, SpeVerificationCollection
from win import Toplevel1
import tkinter as tk
from decimal import Decimal
from companytax.addedtax import addedtax
from companytax.business import business_income_tax
from company import company
from tkinter import *
from companytax.stamp import stamp
from contrast import employment, cloudbusiness
from reward import reward

def main():
    global root
    root = tk.Tk()
    global top
    top = Toplevel1 (root)
    top.Button1.configure(command = caltax)
    top.Button2.configure(command = deleteall)
    top.menubar.add_command(label="使用说明",command = infodisplay)
    deleteall()
    root.mainloop()


#传入一个数字，输出文本格式且保留两位小数的数字
def quantize(number):
    str_number = str(number)
    str_number = Decimal(str_number).quantize(Decimal("0.01"), rounding = "ROUND_HALF_UP")
    return str_number



def caltax():

    if not test():
        deleteentry()
        return 1


    a = round(float(top.Entry1.get()), 2)    #税务筹划金额
    b = round(float(top.Entry1_3.get()), 2)  #灵活用工的服务费比例
    c = round(float(top.Entry1_4.get()), 2)  #云商服务费比例或者按户收费
    d = round(float(top.Entry1_5.get()), 2)  #云商增值税留存比例
    e = round(float(top.Entry1_6.get()), 2)  #云商所得税留存比例
    f = round(float(top.Entry1_7.get()), 2)  #企业财政奖励比例
    g = round(float(top.Entry2.get()), 2)    #企业的收入/成本
    h = round(float(top.Entry1_71.get()), 2)       #商户数量

    i = top.v1.get()    #灵活用工的专票点数
    j = top.v2.get()    #灵活用工的印花税点数
    k = top.v3.get()    #企业的企业所得税的税点
    l = top.v4.get()    #云商个体户计价方式
    m = top.v5.get()    #云商印花税税点
    n = top.v6.get()    #云商的商户核定所得率
    o = top.v7.get()    #企业开出的增值税专票税点
    p = top.v10.get()   #变更计费方式的标签文字


    mysales = a * g    #企业的收入开票金额

    myemployment = employment(sales = a, servicerate = b / 100, addedrate = i, stamprate = j)   #计算灵活用工方案
    allsales = myemployment.allsales                      #灵活用工方案开票的金额
    allmyaddeddeduction = myemployment.myaddedtaxvalue    #灵活用工方案增值税税款,用于进项抵扣
    allmycost = myemployment.myprice                     #灵活用工方案成本
    allmystamptax = myemployment.mystamptax         #灵活用工方案印花税
    allservicesales = myemployment.servicesales     #灵活用工方案的总服务费
    myemploymentcompany = company(sales = mysales, addedrate = o, incomerate = k, stamprate = 0, ahalve = False, shalve = False, addeddeduction = allmyaddeddeduction, cost = allmycost, incomestamptax = allmystamptax)


    myemploymentperson = a / h                 #每户商户收入
    myemploymentVerificationCollection = SpeVerificationCollection(myemploymentperson / 12).PersonalIncomeTax()   #每户商户的全年个税
    allemploymentVerificationCollection = myemploymentVerificationCollection * h                 #所有商户的个税
    myemploymentincome = myemploymentperson - myemploymentVerificationCollection                 #每户商户的实际收入
    allemploymentincome = myemploymentincome * h                                                 #所有商户的实际收入




    mycloudbusinessperson = a / h                 #每户商户年收入，即开票金额
    if l == 0:
        myservicesales = (a / h) * (c / 100)      #按照服务费比例推算云商服务费金额
    elif l == 1:
        myservicesales = c               #按照服务费金额推算云商服务费金额

    mycloudbusiness = cloudbusiness(sales = a, servicesales = myservicesales * h , stamprate = m)
#    mycloudbusinessperson = a / h                             #每户云商商户的收入金额，也就是开票金额
    allmycloudaddeddeduction = mycloudbusiness.myaddedtaxvalue    #金财云商方案增值税税款
    allmycloudcost = mycloudbusiness.myprice                     #金财云商方案成本
    allmycloudstamptax = mycloudbusiness.mystamptax          #金财云商方案印花税
    mycloudbusinesscompany = company(sales = mysales, addedrate = o, incomerate = k, stamprate = 0, ahalve = False, shalve = False, addeddeduction = allmycloudaddeddeduction, cost = allmycloudcost, incomestamptax = allmycloudstamptax)



    if mycloudbusinessperson > 1200000:
       myaddedtax = addedtax(mycloudbusinessperson, 1, 0.03, True)
       myprice = myaddedtax.price            #以不含税价格计算个人所得税
       myaddedtaxvalue = myaddedtax.addedtaxvalue  #增值税税额
       mysurtax = quantize(myaddedtax.additional.surtax())  #附加税税额
       alladdedtaxvalue = myaddedtax.addedtaxvalue + myaddedtax.additional.surtax()  #总税额
       print1 = '代理商税负（增值税）：按照国家规定，小规模纳税人年度销售额未超120万元的免征增值税。单个个体户的年开票金额超过120万，按照需要缴纳增值税进行测算（征收率为3%）。个体户全年经营收入为不含税销售金额合计。单个个体户需要缴纳增值税{}元，需要缴纳附加税{}元，增值税和附加税总额{}元。\n'.format(quantize(myaddedtaxvalue), quantize(mysurtax), quantize(alladdedtaxvalue))



    elif mycloudbusinessperson <= 1200000:
       myprice = mycloudbusinessperson          #以价税合计价格计算个人所得税
       myaddedtaxvalue = 0  #增值税税额
       mysurtax = 0  #附加税税额
       alladdedtaxvalue = 0  #总税额
       print1 = '按照国家规定，小规模纳税人年度销售额未超120万元的免征增值税。单个个体户的年开票金额未超过120万，按照免增值税进行测算。个体户全年经营收入为价税金额合计。单个个体户需要缴纳增值税{}元，需要缴纳附加税{}元，增值税和附加税总额{}元。\n'.format(quantize(myaddedtaxvalue), quantize(mysurtax), quantize(alladdedtaxvalue))







    mycloudbusinessVerificationCollection = VerificationCollection(salary = myprice / 12, social = 0, special = 0, other = 0, legal = 0, collectrate = n).PersonalIncomeTax()   #每户商户的全年个税
    allcloudbusinessVerificationCollection = (alladdedtaxvalue + mycloudbusinessVerificationCollection) * h        #所有商户的税款
    mycloudbusinessincome = mycloudbusinessperson - alladdedtaxvalue - mycloudbusinessVerificationCollection - myservicesales              #每户商户的实际收入
    allcloudbusinessincome = mycloudbusinessincome * h         #所有商户的实际收入


    #云商财政奖励
    myreward = reward(addedtaxvalue = mycloudbusinesscompany.myaddedtaxvalue, businessincometax = mycloudbusinesscompany.myBusinessIncomeTax, personalincometax = 0,
    urban_construction = mycloudbusinesscompany.natadditional.urban_construction , addrewardrate = d/100, busrewardrate = e/100, businessrate = f/100)


    print3 = '企业预计一年向{}个代理商总计发放{}元的金额作为企业成本，平均每个代理商发放{}元。我们将对{}元进行税务筹划，下面的模型将演示使用灵活用工方案和使用金财云商智慧税筹方案的税收分析。\n\n'.format(h, quantize(a), quantize(a / h), quantize(a))
    print4 = '灵活用工税筹方案：\n'
    print5 = '企业发放{}元使用灵活用工方案，灵活用工服务费为{}%，则灵活用工服务供应商为企业开具{}元金额的增值税税率为{}%的专用发票，专用发票的税额{}元可用于企业进行进项抵扣，专用发票实际价格{}元可用于企业计入成本。\n'.format(quantize(a),
    quantize(b),quantize(allsales),i * 100,quantize(allmyaddeddeduction),quantize(allmycost))
    print6 = '假设企业的收入/成本为{},则企业年收入为{}*{}={}元。企业对外开具税率为{}%的增值税专用发票。\n'.format(quantize(g),quantize(a),quantize(g),quantize(mysales),quantize(o * 100))
    print7 = '企业需要缴纳增值税款（销项-进销）{}-{}={}元，附加税款为{}元，印花税款为{}元，所得税款（附加税及印花税均计入成本）为{}元。税款合计{}元。\n'.format(quantize(myemploymentcompany.myaddedtax.addedtaxvalue),
    quantize(myemploymentcompany.addeddeduction),quantize(myemploymentcompany.myaddedtaxvalue),quantize(myemploymentcompany.myadditional),quantize(myemploymentcompany.mystamptax),quantize(myemploymentcompany.myBusinessIncomeTax),
    quantize(myemploymentcompany.alltax))
    print8 = '灵活用工服务供应商向代理商发放金额，按照征收率1.5%代扣代缴个人所得税（月收入3万以下免征）。每个代理商发放{}元需要扣除{}元个税，每个代理商税后收入为{}元。\n\n'.format(
    quantize(a / h),quantize(myemploymentVerificationCollection),quantize(myemploymentincome))
    print9 = '结论：在企业年收入{}元中，全部纳税额（企业税负+代理商税负）为{}元，{}个代理商获取税后收益总计{}元，灵活用工服务供应商获取服务费收益{}元，企业利润收益为{}元。\n'.format(quantize(mysales),
    quantize(myemploymentcompany.alltax + allemploymentVerificationCollection),h,quantize(allemploymentincome),quantize(myemployment.servicesales),quantize(myemploymentcompany.myaferprofit))
    print18 = '灵活用工服务方案中，企业收益+代理商税后收益总和为{}元。\n\n'.format(quantize(allemploymentincome + myemploymentcompany.myaferprofit))


    print10 = '金财云商智慧税筹方案：\n'
    print11 = '企业发放{}元使用金财云商智慧税筹方案，则{}个代理商将注册成为金财云商商户，为企业开具总计{}元金额的普通发票。金财云商为企业开具{}元金额的增值税专用发票。\n'.format(
    quantize(a),h,quantize(a),quantize(mycloudbusiness.servicesales))
    print12 = '假设企业的收入/成本为{},则企业年收入为{}*{}={}元。企业对外开具税率为{}%的增值税专用发票。\n'.format(quantize(g),quantize(a),quantize(g),quantize(mysales),o * 100)
    print13 = '企业需要缴纳增值税款（销项-进销）{}-{}={}元，附加税款为{}元，印花税款为{}元，所得税款（附加税及印花税均计入成本）为{}元。税款合计{}元。\n'.format(quantize(mycloudbusinesscompany.myaddedtax.addedtaxvalue),
    quantize(mycloudbusinesscompany.addeddeduction),quantize(mycloudbusinesscompany.myaddedtaxvalue),quantize(mycloudbusinesscompany.myadditional),quantize(mycloudbusinesscompany.mystamptax),quantize(mycloudbusinesscompany.myBusinessIncomeTax),
    quantize(mycloudbusinesscompany.alltax))
    print14 = '金财云商商户按照{}%的核定所得率征收个人所得税。每个金财云商商户发放{}元需要扣除{}元个税，同时每个金财云商商户需要缴纳{}元服务费。每个代理商税费后收入为{}元。\n'.format(
    n * 100,quantize(a / h),quantize(mycloudbusinessVerificationCollection),quantize(myservicesales),quantize(mycloudbusinessincome))
    print15 = '金财云商智慧税筹方案，企业可获得地方留存税收的{}%作为财政奖励，模型中企业可获得{}元财政奖励收入。\n\n'.format(f,quantize(myreward.businessreward))
    print16 = '结论：在企业年收入{}元中，全部纳税额（企业税负+代理商税负-财政奖励）为{}元，{}个代理商获取税费后收益总计{}元，金财云商智慧税筹供应商获取服务费收益{}元，企业收益+财政奖励为{}+{}+{}={}元。\n'.format(quantize(mysales),
    quantize(mycloudbusinesscompany.alltax + allcloudbusinessVerificationCollection - myreward.businessreward),quantize(h),quantize(allcloudbusinessincome),quantize(myservicesales * h),quantize(mycloudbusinesscompany.myaferprofit),quantize(myservicesales * h),
    quantize(myreward.businessreward),quantize((mycloudbusinesscompany.myaferprofit + myservicesales * h) + myreward.businessreward))
    print19 = '金财云商智慧税筹方案中，企业收益+代理商税后收益总和为{}元，比灵活用工服务方案多出{}元。\n\n'.format(quantize((mycloudbusinesscompany.myaferprofit + myservicesales * h) + myreward.businessreward + allcloudbusinessincome),
    quantize((mycloudbusinesscompany.myaferprofit + myservicesales * h) + myreward.businessreward + allcloudbusinessincome - allemploymentincome - myemploymentcompany.myaferprofit))
    print17 = '结论（不含财政奖励）：在企业年收入{}元中，全部纳税额（企业税负+代理商税负）为{}元，{}个代理商获取税费后收益总计{}元，金财云商智慧税筹供应商获取服务费收益{}元，企业收益为{}+{}={}元。\n'.format(quantize(mysales),
    quantize(mycloudbusinesscompany.alltax + allcloudbusinessVerificationCollection),h,quantize(allcloudbusinessincome),quantize(myservicesales * h),quantize(mycloudbusinesscompany.myaferprofit),
    quantize(myservicesales * h),quantize(mycloudbusinesscompany.myaferprofit + myservicesales * h))
    print20 = '金财云商智慧税筹方案（不含财政奖励）中，企业收益+代理商税后收益总和为{}元，比灵活用工服务方案多出{}元。\n\n'.format(quantize(mycloudbusinesscompany.myaferprofit + myservicesales * h + allcloudbusinessincome),
    quantize((mycloudbusinesscompany.myaferprofit + myservicesales * h) + allcloudbusinessincome - allemploymentincome - myemploymentcompany.myaferprofit))



    top.Text1.configure(state='normal')
    top.deletetext()
    top.Text1.insert('insert', print3, "tag_1")
    top.Text1.insert('insert', print4, "tag_2")
    top.Text1.insert('insert', '企业成本：', "tag_2")
    top.Text1.insert('insert', print5)
    top.Text1.insert('insert', '企业收入：', "tag_2")
    top.Text1.insert('insert', print6)
    top.Text1.insert('insert', '企业税负：', "tag_2")
    top.Text1.insert('insert', print7)
    top.Text1.insert('insert', '代理商税负：', "tag_2")
    top.Text1.insert('insert', print8)
    top.Text1.insert('insert', print9, "tag_1")
    top.Text1.insert('insert', print18, "tag_1")
    top.Text1.insert('insert', '***********************************\n' )
    top.Text1.insert('insert', print10, "tag_2")
    top.Text1.insert('insert', '企业成本：', "tag_2")
    top.Text1.insert('insert', print11)
    top.Text1.insert('insert', '企业收入：', "tag_2")
    top.Text1.insert('insert', print12)
    top.Text1.insert('insert', '企业税负：', "tag_2")
    top.Text1.insert('insert', print13)
    top.Text1.insert('insert', '代理商税负（增值税）：', "tag_2")
    top.Text1.insert('insert', print1)
    top.Text1.insert('insert', '代理商税负（个人所得税）及服务费：', "tag_2")
    top.Text1.insert('insert', print14)
    top.Text1.insert('insert', '企业收入（财政奖励）：', "tag_2")
    top.Text1.insert('insert', print15)
    top.Text1.insert('insert', print16, "tag_1")
    top.Text1.insert('insert', print19, "tag_1")
    top.Text1.insert('insert', print17, "tag_1")
    top.Text1.insert('insert', print20, "tag_1")
    top.Text1.configure(state='disabled')


def deleteall():
    top.Text1.configure(state='normal')
    top.deleteentry2()
    top.deletetext()

    top.Text1.insert('insert', '金财互联平台（SZ002530），通过打造智慧化的财税服务新体验，帮助企业实现“合规、降负、增利”，致力于提升小微企业主的获得感和幸福感。\n')
    top.Text1.insert('insert', '***********************************\n' )
    top.Text1.insert('insert', '本模型主要用于企业使用灵活用工平台与使用金财云商智慧税筹平台的纳税和收入比较模型测算，可用于税筹企业测算灵活用工平台与金财云商平台的收益模型。\n')
    top.Text1.insert('insert', '***********************************\n' )
    top.Text1.insert('insert', '本模型由个人开发，数据未经过严格测试，故可能存在BUG或错漏，演示数据仅供参考。如您发现问题请联系开发者Near进行软件修正和更新（微信号Near-river）。\n' , "tag_2")
    top.Text1.insert('insert', '***********************************\n' )
    top.Text1.insert('insert', '如您对金财云商智慧税筹解决方案感兴趣，请联系金财互联销售人员，金财互联税筹专家团队将竭诚为您提供专业、可靠、贴心的税筹服务。\n\n' )
    top.Text1.insert('insert', '测算说明：\n', "tag_2")
    top.Text1.insert('insert', '1、税务筹划金额指企业准备发给全部代理商的总金额，收入/成本系数指企业的营业收入和税务筹划金额的比值。\n' )
    top.Text1.insert('insert', '2、企业专票税点指企业取得营业收入对外开除的增值税专用发票税点。\n' )
    top.Text1.insert('insert', '3、企业所得税计算中，进项发票金额（普票的价税合计或专票的实际价格）、附加税、印花税计入企业成本。\n' )
    top.Text1.insert('insert', '4、灵活用工平台服务费指灵活用工平台代收取的基于税务筹划金额一定比例的服务费，通常灵活用工平台会开具税务筹划金额+服务费金额的增值税专用发票给到企业。\n' )
    top.Text1.insert('insert', '5、灵活用工平台个人所得税采用征收率1.5%（月收入3万以下免征）模式进行测算。\n' )
    top.Text1.insert('insert', '6、金财云商智慧税筹平台财政奖励金额中，计入增值税地方留存比例、所得税地方留存比例及城建税（100%计入）。\n' )
    top.Text1.insert('insert', '7、金财云商智慧税筹平台服务费由个体户缴纳，但服务费开具6%增值税金额专票给到企业进行增值税、所得税抵扣，因此企业收益会大于账面利润（此处可详询金财互联税筹专家团队）。\n' )
    top.Text1.insert('insert', '8、金财云商智慧税筹平台个人所得税适用生产经营所得的个人所得税税率。\n' )
    top.Text1.configure(state='disabled')



def t_close_handler():
    root.attributes("-disabled", 0)
    f1.destroy()


def infodisplay():
    root.attributes("-disabled", 1)
    global f1
    f1 = Toplevel(root)
    # f1.config(width=710,height=510)
    f1.geometry("997x214+417+205")                             #("671x182+287+246")
    f1.title("平台型公司税负及盈利情况测模型")
    f1.resizable(0, 0)
    f1.protocol("WM_DELETE_WINDOW", t_close_handler)
    Text1 = Text(f1)
    #Label_1 = Label(f1)
    Text1.place(relx=0.04, rely=0.093, relheight=0.794, relwidth=0.937)
    Text1.configure(background="#d9d9d9")
    Text1.configure(state='normal')
    Text1.insert('insert', '金财云商与灵活用工收益比较测算模型由金财互联陈阳个人制作，软件可自由散发使用。\n')
    Text1.insert('insert', '该模型未经过严格测试，故仅供参考。开发者不承担因数据不准确引发的任何问题。\n')
    Text1.insert('insert', '如您发现模型存在问题或与开发者交流，欢迎您添加微信号Near-river与软件开发者联系。感谢您的使用！！\n')
    Text1.insert('insert', '***********************************\n' )
    Text1.insert('insert', '***********************************\n' )
    Text1.insert('insert', 'V1.0版本说明（20201109）：\n')
    Text1.insert('insert', '软件发布\n')
    Text1.insert('insert', 'V2.0版本说明（20201202）：\n')
    Text1.insert('insert', '1.测算模型增加了收入/成本系数和财政奖励系数\n')
    Text1.insert('insert', '2.修改测算模型为直接测算企业的税收\n')
    #Text1.configure(text='''说明：个税税筹计算器由陈阳个人制作，软件可自由散发使用。\n该计算器数据未经过严格测试，故仅供参考。开发者不承担因数据不准确引发的任何问题。\n如您发现软件存在问题或与开发者交流，欢迎您添加微信号Near-river与作者联系。''')
    Text1.configure(state='disabled')
    scrol = Scrollbar(f1)
    scrol.pack(side="right", fill="y")
    Text1.configure(yscrollcommand = scrol.set)
    scrol.configure(command=Text1.yview)



def test():
    try:  # 如果能运行float(s)语句,继续
        float(top.Entry1.get())
        pass
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        return False
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(top.Entry1_3.get())
        pass
    except ValueError:
        return False
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(top.Entry1_4.get())
        pass
    except ValueError:
        return False
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(top.Entry1_5.get())
        pass
    except ValueError:
        return False
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(top.Entry1_6.get())
        pass
    except ValueError:
        return False
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(top.Entry1_7.get())
        pass
    except ValueError:
        return False
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(top.Entry2.get())
        pass
    except ValueError:
        return False
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        int(top.Entry1_71.get())
        pass
    except ValueError:
        return False


    if top.v4.get() == 0:
        if float(top.Entry1_4.get()) > 100:
            return False


    if float(top.Entry1.get()) < 0:
        return False
    elif float(top.Entry1_3.get()) < 0:
        return False
    elif float(top.Entry1_4.get()) < 0:
        return False
    elif float(top.Entry1_5.get()) < 0:
        return False
    elif float(top.Entry1_6.get()) < 0:
        return False
    elif float(top.Entry1_7.get()) < 0:
        return False
    elif float(top.Entry2.get()) < 0:
        return False
    elif float(top.Entry1_71.get()) < 0:
        return False


    elif float(top.Entry1.get()) > 1000000000000:
        return False
    elif float(top.Entry1_3.get()) > 100:
        return False
#    elif float(top.Entry1_4.get()) > 100:
#        if top.v4.get() == 0:
#            return False
    elif float(top.Entry1_4.get()) >= 10000:
        return False
    elif float(top.Entry1_5.get()) > 100:
        return False
    elif float(top.Entry1_6.get()) > 100:
        return False
    elif float(top.Entry1_7.get()) > 100:
        return False
    elif float(top.Entry2.get()) > 50:
        return False
    elif float(top.Entry1_71.get()) >= 100000:
        return False
    return True


def deleteentry():

    top.Entry1.delete(0, "end")
    top.Entry1.insert(0,'32000000')

    top.Entry1_3.delete(0, "end")
    top.Entry1_3.insert(0,'6.72')

    top.Entry1_4.delete(0, "end")
    top.Entry1_4.insert(0,'1000')

    top.Entry1_5.delete(0, "end")
    top.Entry1_5.insert(0,'50')

    top.Entry1_6.delete(0, "end")
    top.Entry1_6.insert(0,'40')

    top.Entry1_7.delete(0, "end")
    top.Entry1_7.insert(0,'70')

    top.Entry2.delete(0, "end")
    top.Entry2.insert(0,'1.1')

    top.Entry1_71.delete(0, "end")
    top.Entry1_71.insert(0,'250')

    top.v4.set(1)

    tk.messagebox.showerror('输入错误提示', '输入的数字超出管控范围，请检查检查您的输入……')


if __name__ == '__main__':
    main()
