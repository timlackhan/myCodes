from pyspark import SparkContext, SparkConf,StorageLevel
from datetime import *
import time
from operator import add
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.regression import LabeledPoint
import json



# Load and parse the data
def parsePoint(line):
        values = [float(x) for x in line.split(',')]
        return LabeledPoint(values[0], values[1:])


#read json data from original data
def readJson(t):
	t=t.split("{")
	r=""
	length=len(t)
	for i in range(1,length):
		r=r+"{"+t[i]
        return r


#split the json data
def splitJson(line):
        json_str=json.loads(line)
        return str(json_str["adslot_id"]).replace(",",";")+","+str(json_str["creative_id"]).replace(",",";")+","+str(json_str["advertiser_id"]).replace(",",";")+","+str(json_str["adslot_pos"]).replace(",",";")+","+str(json_str["creative_size"]).replace(",",";")+","+str(json_str["localtime"]).replace(",",";")+","+str(json_str["geo"]).replace(",",";")+","+str(json_str["adx"]).replace(",",";")+","+str(json_str["devicetype"]).replace(",",";")+","+str(json_str["platform"]).replace(",",";")+","+str(json_str["os"]).replace(",",";")+","+str(json_str["browser"]).replace(",",";")+","+str(json_str["impct"]).replace(",",";")+","+str(json_str["impid"]).replace(",",";")

#replace null with -1
def replaceNull(line):
        fields=line.split(",")
        res=""
        for i in range(0,len(fields)):
                if fields[i]=='':
                        fields[i]=-1
                res=res+str(fields[i])+","
        res=res[:-1]
        return res

#process date
def processDate(field):
        fields=field.split(",")
        dateAndTime=fields[5]
        date=dateAndTime.split(" ")[0].split("-")[2]
        time=dateAndTime.split(" ")[1].split(":")[0]
        return fields[0]+","+fields[1]+","+fields[2]+","+fields[3]+","+fields[4]+","+date+","+time+","+fields[6]+","+fields[7]+","+fields[8]+","+fields[9]+","+fields[10]+","+fields[11]+","+fields[12]+","+fields[13]

#get rid of feature impid and add label0
def addLabel0(field):
        fields=field.split(",")
        return "0,"+fields[0]+","+fields[1]+","+fields[2]+","+fields[3]+","+fields[4]+","+fields[5]+","+fields[6]+","+fields[7]+","+fields[8]+","+fields[9]+","+fields[10]+","+fields[11]+","+fields[12]+","+fields[13]

#get rid of feature impid and add label1
def addLabel1(field):
        fields=field.split(",")
        return "1,"+fields[0]+","+fields[1]+","+fields[2]+","+fields[3]+","+fields[4]+","+fields[5]+","+fields[6]+","+fields[7]+","+fields[8]+","+fields[9]+","+fields[10]+","+fields[11]+","+fields[12]+","+fields[13]


#save weights and intercept
def save_to_file(file_name, contents):
        fh = open(file_name, 'a')
        fh.write(contents)
        fh.close()


# deal with the date field
# input:2017 04 20(date)
# output:4(week)
def DayToWeek(y, m, d):
        c = y / 100
        y = y % 100
        if m == 1 or m == 2:
                m += 12
                y -= 1
        return (y + y / 4 + c / 4 - 2 * c + (26 * (m + 1) / 10) + d - 1) % 7


# data coding
# we will not process the first field x[0] (label)
# for x[6] (pday),we have input date and we will output week
# for x[7] (phour),we will judge its time and have output{0,1}
# for x[1,4,6,9,12,13,14] (adslot_id,advertiser_id,creative_size,geo,platform,os,browser) we will have one-spot encoding
# and for other fields,we won't have any processing
# for every line in the logs,it will be outputed as a string (neostr)

def func(x):
    neostr = "" + str(x[0])
    pointer = 0
    for j in range(1, 15):
        temp = ""
        endder = ""

        if j == 6:
            day = int(x[j])
            weekday = DayToWeek(int(todayYear),int(todayMonth),day)
            if weekday >= 1 and weekday <= 5:
                neostr = neostr + ",1"
            else:
                neostr = neostr + ",0"

        elif j == 7:
            hour = int(x[j])
            if hour >= 17 and hour <= 21:
                neostr = neostr + ",1"
            else:
                neostr = neostr + ",0"


        elif j == 1 or j == 3 or j == 5 or j == 8 or j == 11 or j == 12 or j == 13:
            endder=",1"
            for i in range(0, len(broadcastVar[pointer].value)):
                if x[j] == broadcastVar[pointer].value[i]:
                    temp = temp + ",1"
                    endder = ",0"
                else:
                    temp = temp + ",0"
            temp = temp + endder
            neostr = neostr + temp
            pointer += 1

        else:
            neostr = neostr + "," + str(x[j])
    return neostr


# save the fields after processing
# eg.result is "label,baidu_1,baidu_2,...."
# result will be saved as a string (neostr)
def attr(x):
    neostr = ""
    neostr = neostr + "label"
    for i in range(0, len(broadcastVar[0].value)):
        neostr = neostr + ",adslot_id__" + str(broadcastVar[0].value[i])
    neostr = neostr + ",other adslot_id,creative_id"
    for i in range(0, len(broadcastVar[1].value)):
        neostr = neostr + ",advertiser_id__" + str(broadcastVar[1].value[i])
    neostr = neostr + ",other advertiser_id,adslot_pos"
    for i in range(0, len(broadcastVar[2].value)):
        neostr = neostr + ",creative_size__" + str(broadcastVar[2].value[i])
    neostr = neostr + ",other creative_size,pday,phour"
    for i in range(0, len(broadcastVar[3].value)):
        neostr = neostr + ",geo__" + str(broadcastVar[3].value[i])
    neostr = neostr + ",other geo,adx,devicetype"
    for i in range(0, len(broadcastVar[4].value)):
        neostr = neostr + ",platform__" + str(broadcastVar[4].value[i])
    neostr = neostr + ",other platform"
    for i in range(0, len(broadcastVar[5].value)):
        neostr = neostr + ",os__" + str(broadcastVar[5].value[i])
    neostr = neostr + ",other os"
    for i in range(0, len(broadcastVar[6].value)):
        neostr = neostr + ",browser__" + str(broadcastVar[6].value[i])
    neostr = neostr + ",other browser,impct"
    return neostr





if __name__ == "__main__":

	start=time.time()
	today=str(date.today())
        todayYear = today.split("-")[0]
        todayMonth = today.split("-")[1]
        todayDay = today.split("-")[2]
        #winRead = "/nginxlog/10.10.241.225/" + todayYear + "-" + todayMonth + "*/" + todayYear + "-" + todayMonth + "*/*3.log.lzo"
        #clickRead = "/nginxlog/10.10.241.225/" + todayYear + "-" + todayMonth + "*/" + todayYear + "-" + todayMonth + "*/*5.log.lzo"

	winRead = "hdfs://10.11.1.42:9000/timlackhan/2017-07-11/3/*3.log"
        clickRead = "hdfs://10.11.1.42:9000/timlackhan/2017-07-11/5/*5.log"
        attrLocalWrite = '/home/admin/timlackhan/attrs2_ctr'
        weightsWrite='/home/admin/timlackhan/weights2_ctr'
        combinationWrite='/home/admin/timlackhan/combination2_ctr'
	resTime='/home/admin/timlackhan/longtime_ctr'
        p=0.8


        # loc is the number of the line we want to deal with
        # we set the threshold for the fields

        loc = {0: 1, 1: 3, 2: 5, 3: 8, 4: 11, 5: 12, 6: 13}
        threshold = {2: 0, 4: 0, 6: 0, 9: 0, 12: 0, 13: 0, 14: 0}


        # open spark
        # set master node is spark://10.11.1.42:7077
        conf = SparkConf().setAppName("cleanData")
        sc = SparkContext(conf=conf)

        # read log from hdfs
        clickLog = sc.textFile(clickRead)
	#clickLog.persist(StorageLevel.MEMORY_AND_DISK_SER)
	clickCount=clickLog.count()
	#clickProp=1.0*10000/clickCount
	clickLog=clickLog.map(readJson).map(splitJson)
	#clickLog=clickLog.sample(False,clickProp).map(readJson).map(splitJson)
	clickLog=clickLog.map(replaceNull).map(processDate)
        winLog = sc.textFile(winRead)
	#winLog.persist(StorageLevel.MEMORY_AND_DISK_SER)
	#winProp=1.0*50000/winLog.count()

	#winLog.count()
	time1=time.time()
	save_to_file(resTime,"time1="+str(time1-start)+"\n")


	winLog=winLog.map(readJson).map(splitJson).map(replaceNull).map(processDate)
	
	#winLog.count()
	time2=time.time()
	save_to_file(resTime,"time2="+str(time2-time1)+"\n")	

	#winLog=winLog.sample(False,winProp).map(readJson).map(splitJson).map(replaceNull).map(processDate)

        # read impid field
        clickList = clickLog.map(lambda field: field.split(",")[14]).collect()
	
        # divide the log into label0 and label1
        winLog0 = winLog.filter(lambda field: field.split(",")[14] not in clickList).map(addLabel0)
        winLog1 = winLog.filter(lambda field: field.split(",")[14] in clickList).map(addLabel1)
	
        clickLog = clickLog.map(addLabel1)
        #get data(pos vs neg:1 vs 1)
        proportion=float(1.0*(clickCount+winLog1.count())/winLog0.count())
	
	time3=time.time()
	save_to_file(resTime,"time3="+str(time3-time2)+"\n")

        winLog0_1vs1 = winLog0.sample(False, proportion)
	
        log_1vs1 = clickLog.union(winLog1).union(winLog0_1vs1)
	#log_1vs1=clickLog.union(winLog1).union(winLog0)

	#log_1vs1.count()
	time4=time.time()
	save_to_file(resTime,"time4="+str(time4-time3)+"\n")

	#log_1vs1=log_1vs1.persist(StorageLevel.MEMORY_AND_DISK_SER)
	#clickLog.unpersist()
	#winLog.unpersist()
	


	broadcastVar = range(7)

        #set threshold for one-hot spot
        for i in range(7):
	    prequesition=log_1vs1.map(lambda line: (line.split(",")[loc[i]], 1))
	    prequesition=prequesition.reduceByKey(add)
	    prequesition=prequesition.sortBy(lambda x: x[1],False)
            count = int(prequesition.count() * p) + 1
	    l = prequesition.map(lambda x:x[0]).take(count)
	    broadcastVar[i]=sc.broadcast(l)
            
	time5=time.time()
	save_to_file(resTime,"time5="+str(time5-time4)+"\n")

        # we use python2 so we have to encode the data
        dataEncode = log_1vs1.map(lambda x: x.encode("utf-8").split(","))	


        # deal with the  data

        resultLog_1vs1 = dataEncode.map(func)
	#resultLog_1vs1.saveAsTextFile("hdfs://10.11.1.42:9000/timlackhan/resultLog_1vs1")

        #save the attributes
        attrRes = attr("1")
        save_to_file(attrLocalWrite,attrRes)

        # process the data pattern
        parsedData = resultLog_1vs1.map(parsePoint)

	#parsedData.count()
	time6=time.time()
	save_to_file(resTime,"time6="+str(time6-time5)+"\n")

        # Build the model
        lrm = LogisticRegressionWithLBFGS.train(parsedData)

	time7=time.time()
	save_to_file(resTime,"time7="+str(time7-time6)+"\n")

        # define st for saving the weights of the model
        st = ""

        # the weights of the model
        w = lrm.weights

        # the total number of the weights
        s = w.size

        # give the total weights to st
        st = st + str(w[0])
        for i in range(1, s):
                st = st + "," + str(w[i])
        st = st + "," + str(lrm.intercept)

        # save the weights
        save_to_file(weightsWrite,st)


        #combine the attrs with weights
        input = open(attrLocalWrite)
        line = input.readline()
        list1 = line.split(",")
        list1 = list1[1:]

        input2 = open(weightsWrite)
        line2 = input2.readline()
        list2 = line2.split(",")
        list2 = list2[:-1]

        res = ""
        for i in range(0, len(list1)):
                res = res + str(list1[i]) + "\t" + str(list2[i]) + "\n"

        save_to_file(combinationWrite, res)

	time8=time.time()
	save_to_file(resTime,"time8="+str(time8-time7)+"\n")

	end=time.time()
	save_to_file(resTime,"whole="+str(end-start)+"\n")

        sc.stop()

