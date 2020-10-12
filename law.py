from bs4 import BeautifulSoup
import requests
import warnings

warnings.filterwarnings("ignore")

#检索关键字返回网页搜索结果
mode = input("请输入检索模式 按标题检索/按正文检索(1/2):")
if(mode=='1') :  flag = "Title"
else : flag = "" 
str = input("请输入需要检索的关键字：")
url_search = 'http://search.chinalaw.gov.cn/SearchLaw{}?effectLevel=2&SiteID=124&PageIndex=&Sort=PublishTime&Query={}&Type=1'.format(flag,str)
response_search = requests.get(url_search)
soup_search = BeautifulSoup(response_search.content.decode('utf-8'),'lxml')
print(soup_search.find('div',class_='searTit').text)			#输出检索结果
if(soup_search.find('span',id='pagecount')==None) : num_page = 2
else : num_page = (int)(soup_search.find('span',id='pagecount').text)
pd = input("请问是否选择全部下载(y/n)：")
if(pd=='y'):
	for page_search in range(1,num_page+1):
		url_result = 'http://search.chinalaw.gov.cn/SearchLaw{}?effectLevel=2&SiteID=124&PageIndex={}&Sort=PublishTime&Query={}&Type=1'.format(flag,page_search,str) 
		response_result = requests.get(url_result)
		soup_result = BeautifulSoup(response_result.content.decode('utf-8'),'lxml')
		for each_result in soup_result.find_all('div',class_='listCon clearself'):
			tip = each_result.find('a')
			link = tip.get('href')
			url = 'http://search.chinalaw.gov.cn/{}'.format(link)
			response = requests.get(url)
			soup = BeautifulSoup(response.content.decode('utf-8'),'lxml')
			if(soup.text == "法规不存在!") : 
				print("法规不存在!")
				continue;
			if(soup.find('span',id='pagecount')==None): num = 1
			else : num = (int)(soup.find('span',id='pagecount').text)
			name = soup.find('div',class_='conTit').text
			os = open('{}.txt'.format(name),'w',encoding='utf-8')
			for i in range(1,num+1):
				url_get_context = url+'PageIndex={}'.format(i)
				response1 = requests.get(url_get_context)
				soup1 = BeautifulSoup(response1.content.decode('utf-8','lxml'))
				body = soup1.find('div',class_='detailCon').find('div','con')
				os.write(body.text)
			print(name+" 已下载")
	print("下载完成")
