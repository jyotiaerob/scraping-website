import requests
from bs4 import BeautifulSoup
import json

import pymongo											#MOngodb database code
from pymongo import MongoClient
client=MongoClient('localhost',27017)


headers={'User-Agent':'Mozilla/5.0'}

base_url="http://startupstash.com/"
req_home_page=requests.get(base_url,headers=headers)
soup=BeautifulSoup(req_home_page.text, "html5lib")
links_tag=soup.find_all('li', {'class':'categories-menu-item'})
titles_tag=soup.find_all('span',{'class':'name'})


"""Below code brings out the Front page pysh links to got the next page  """
frontpage_link=[link.a.get('href').encode('utf-8') for link in links_tag ]   #FRONT PAGE LINK TO NEXT PAGES
print "HOME PAGE links are :>>",frontpage_link 

"""THis below code give the titles of the category pages"""
frontpage_title=[title.getText().encode('utf-8') for title in titles_tag ]	#NAMES OF CATEGORIES 
print "HOME PAGE TITLES ARE :>>",frontpage_title

"""Now from here we will start iterating,first we are going to next page and trying to highlight the 10 links they are providing"""
for i in range(0,len(frontpage_link)):
	req_inside_page = requests.get(frontpage_link[i],headers=headers)
	page_store =BeautifulSoup(req_inside_page.text, "html5lib")
	jump_to_next=page_store.find_all('div', { 'class' : 'company-listing-more' })
	links_per_page=[div.a.get("href").encode('utf-8') for div in jump_to_next]
	print "LINKS IN EVERY CATEGORIES:>>",links_per_page							#all links contains within the website 


	"""Here we will move to each link and extarct the details about the specific targeted website"""
	for j in range(0,len(links_per_page)):
		req_final_page=requests.get(links_per_page[j],headers=headers)
		page_stored=BeautifulSoup(req_final_page.text,'html5lib')
		detail_content=page_stored.find('div', { 'class' : 'company-page-body body'})
		website_detail=[content.string for content in detail_content]
		print "DETAIL ABOUT THE EACH WEBSITE :>>",website_detail	

		"""In the same way here we will extract the Name,Email,and website for that targeted link"""
		detail_website=page_stored.find('div',{'id':"company-page-contact-details"})
		table=detail_website.find('table')
		contact_detail=[col.text.encode('utf-8') for row in table.find_all('tr') for col in row.find_all("td")[1:] ]
		print contact_detail

		"""Here we will extarct the social media link for that particular website eg. facebook,google plus,twitter"""
		page_social=page_stored.find('div',{"class":"company-page-social"})
		social_link=[link.get('href').encode('utf-8') for link in page_social.find_all('a')]
		print social_link

"""TRying to save those result in mongo db database"""
db=client.website_scrapin
cgollection=db.scraprweb
post={'SCRAPEDRESULTS':[frontpage_link,
						frontpage_title,
						{"Category website":links_per_page},
						{"website Detail":website_detail},{"contacts":contact_detail,"Social":social_link}]}