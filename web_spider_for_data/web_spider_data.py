import requests
import re

import importlib,sys
importlib.reload(sys)
# sys.setdefaultencoding("utf-8")

spot_webpage=[]


class spider(object):
	def __init__(self):
		print ("begin" )


	def getsource(self,url):
		html = requests.get(url)
		return html.text

	def changepage(self,url,total_page):
		page_group = []
		page_group.append(url)
		for i in range(2,total_page+1):
			link = re.sub('jingdian','jingdian-1-%s'%i,url,re.S)
			page_group.append(link)
		return page_group


	def geteveryclass(self,source):
		everyclass = re.findall('(li class="item" data-lat.*?</li>)',source,re.S)
		return everyclass
 

	def getinfo(self,eachclass):
		info = {}
		info['spot'] = re.search('class="cn_tit">(.*?)<span class="en_tit">',eachclass,re.S).group(1)
		info['lat']= re.search('data-lat="(.*?)"',eachclass,re.S).group(1)
		info['long']= re.search('data-lng="(.*?)">',eachclass,re.S).group(1)
		info['webpage']=re.search('href="(.*?)"><span class',eachclass,re.S).group(1)
		spot_webpage.append(info['webpage'])
		return info

	def getdetailedinfo(self,eachurl,infor):
		titlepart = re.findall('(<div class="b_title clrfix">.*?</div>)',eachurl,re.S)
		title = re.findall('<h1 class="tit">(.*?)<span class="entit">',titlepart[0],re.S)
		infor['spot']=title[0]
		scorepart = re.findall('(<div class="e_focus_txtbox">.*?<div class="countbox">)',eachurl,re.S)
		addrpart = re.findall('(<div class="e_summary_list_box">.*?<div class="b_detail_section b_detail_ticket")',eachurl,re.S)
		return scorepart,addrpart

	def getscore(self,score,infor):

		rating = re.search('<span class="cur_score">(.*?)</span>',score[0],re.S).group(1)
		time = re.search('<div class="time">(.*?)</div></div>',score[0],re.S).group(1)
		infor["score"]=rating
		infor["suggested time"]=time

		return rating,time


	def getaddr(sef,addr,infor):
		location = re.search('<dd><span>(.*?)</span></dd>',addr[0],re.S).group(1)
		infor["address"]=location

		return location

	def saveinfo(self,classinfo):
		f = open('infojingdian.txt','a')
		for each in classinfo:
			f.writelines('spot:' + each['spot'] + '\n')
			f.writelines('lat:' + each['lat'] + '\n')
			f.writelines('long:' + each['long'] + '\n')
			f.writelines('webpage:' + each['webpage'] + '\n')
		f.close()

	def savedetail(self,spotinfo):
		f=open('detailinfo.txt','a')
		for each in spotinfo:
			f.writelines('spot:' +each['spot']+'\n')
			f.writelines('score:' + each['score'] + '\n')
			f.writelines('suggested time:' + each['time'] + '\n')
			f.writelines('address:' + each['address'] + '\n')




if __name__ == '__main__':
	datainfo=[]
	url = 'https://travel.qunar.com/p-cs299914-beijing-jingdian'
	jikespider = spider()  
	all_links = jikespider.changepage(url,2)
	
	for link in all_links:
		print ("handling " + link)
		print("\n")
		html = jikespider.getsource(link)
		everyclass = jikespider.geteveryclass(html)
		for each in everyclass:
			info = jikespider.getinfo(each)
			datainfo.append(info)


	detailed_data=[]
	for spots in spot_webpage:
		infor={}
		html1 = jikespider.getsource(spots)	
		score,addr = jikespider.getdetailedinfo(html1,infor)
		rating,time = jikespider.getscore(score,infor)
		location = jikespider.getaddr(addr,infor)
		print(infor)
		detailed_data.append(infor)
		print("\n")




















