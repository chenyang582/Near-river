



def main():
    a = reward(addedtaxvalue = 1978301.89, businessincometax = 183575.47, urban_construction = 138481.13, addrewardrate = 0.5, busrewardrate = 0.4, businessrate = 0.7, personalincometax = 0)
    print(a.businessreward)


class reward():
    def __init__(self, addedtaxvalue, businessincometax, urban_construction, addrewardrate, busrewardrate, businessrate, personalincometax = 0):
        self.addedtaxvalue = addedtaxvalue      #增值税总额
        self.businessincometax = businessincometax   #企业所得税总额
        self.personalincometax = personalincometax     #个人所得税总额
        self.urban_construction = urban_construction   #城建税总额

        self.leaveaddedtaxvalue = addedtaxvalue * addrewardrate    #增值税地方留存金额
        self.leavebusinessincometax = businessincometax * busrewardrate    #企业所得税留存金额
        self.leavepersonalincometax = personalincometax * busrewardrate    #个人所得税流留存金额

        self.businessreward = (self.leaveaddedtaxvalue + self.leavebusinessincometax + self.urban_construction) * businessrate  #企业奖励金额，不考虑个税



if __name__ == '__main__':
    main()
