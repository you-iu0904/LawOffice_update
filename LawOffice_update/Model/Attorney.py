class Attorney() :
    def __init__(self,fee_earners,initials,sex,title,admitted_time,hourly_rate):
        self.fee_earners=fee_earners #律师姓名
        self.initials = initials #姓名缩写
        self.sex = sex #性别
        self.title = title #职位
        self.admitted_time = admitted_time #认证时间
        self.hourly_rate = hourly_rate #收费时间(Hrs)
    #保存数据
    def save(self,file,usr_dict):
        data=[]
        data.append(self.initials)
        data.append(self.admitted_time)
        data.append(self.title)
        data.append(self.sex)
        data.append(self.hourly_rate)
        usr_dict[self.fee_earners]=data
        fileobj=open(file,'w')
        fileobj.write(str(usr_dict))
        fileobj.close()



