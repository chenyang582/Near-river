from companytax.addedtax import addedtax
from companytax.business import business_income_tax
from companytax.stamp import stamp




def main():
    a = employment(1000, 0.08, 0.06, 0.001, 0.15)
    b = cloudbusiness(1000, 500, 0.001, 0.15)
    print(a.myaddedtaxvalue)
    print(a.mystamptax)
    print(a.myincome)
    print(b.myaddedtaxvalue)
    print(b.mystamptax)
    print(b.myincome)





class employment():
    def __init__(self, sales, servicerate, addedrate, stamprate):
        self.sales = sales      #税务筹划金额（不含税）
        self.servicesales = sales * servicerate     #服务费金额
        self.allsales = self.sales + self.servicesales    #灵活用工平台开票金额
        self.myaddedtax = addedtax(self.allsales, companytype = 0, rate = addedrate, halve = False)  #增值税
        self.myprice = self.myaddedtax.price    #不含税价格
        self.myaddedtaxvalue = self.myaddedtax.addedtaxvalue    #增值税税额
        self.mystamp = stamp(sales = self.allsales, halve = False, rate = stamprate)   #印花税   企业应缴纳的印花税
        self.mystamptax = self.mystamp.stamptax   #印花税税额
#        self.mybusiness = business_income_tax(sales = self.myprice, cost = 0, rate =  incomerate)   #所得税，成本可减少的数额
#        self.myincome =self.mybusiness.BusinessIncomeTax    #所得税成本减少的数额


class cloudbusiness():
    def __init__(self, sales, servicesales, stamprate):
        self.sales = sales                       #税务筹划金额，开多张普票
        self.servicesales = servicesales         #服务费金额
        self.allsales = self.sales + self.servicesales
        self.myaddedtax = addedtax(self.servicesales, companytype = 0, rate = 0.06, halve = False)  #服务费开具增值税专票，税率按0.06计算
        self.myprice = self.myaddedtax.price + self.sales   #服务费的不含税价格和云商商户开具的发票价税合计总和
        self.myaddedtaxvalue = self.myaddedtax.addedtaxvalue    #服务费的增值税税额，用于抵扣
        self.mystamp = stamp(sales = sales, halve = False, rate = stamprate)   #印花税
        self.mystamptax = self.mystamp.stamptax   #印花税税额
#        self.mybusiness = business_income_tax(sales = self.allsales, cost = 0, rate =  incomerate)   #所得税，成本可减少的数额
#        self.myincome = self.mybusiness.BusinessIncomeTax    #所得税成本减少的数额


if __name__ == '__main__':
    main()
