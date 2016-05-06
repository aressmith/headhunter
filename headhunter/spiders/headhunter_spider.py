import scrapy
from headhunter.items import headhunterItem


class headhunterSpider(scrapy.Spider):
   name = 'headhunter'
   #allowed_domains = ["dice.com"]
   start_urls = [	
   ]
   
   def __init__(self):
      # NOTE: need to add multiple name functionality later
      companyName = raw_input("Enter company name: ")
      companyName = companyName.replace(" ", "+")
      self.start_urls.append("https://www.dice.com/jobs?q=company:(" + companyName + ")")
      self.start_urls.append("http://www.careerbuilder.com/employerprofile/companysearch.aspx?compsearch=" + companyName + "&sortby=jobcount")
      #xpath('//span/a[@id="company0"]/@href').extract()[1]
      
   def parse(self, response):
      for url in self.start_urls:
	if url.find("dice.com"):
	  jobList = response.xpath('//a[contains(@id, "position")]/@href')
	if url.find("careerbuilder"):
	  print "\c builder"
	  #yield scrapy.Request(response.xpath('//a[contains(text(), "view active jobs")]/@href').extract())
	  
	  #NOTE: use this on the link given above for careerbuilder
	  #response.xpath('//a[contains(@id, "JobTitleLink")]')
	
	if jobList:
	  for href in jobList:
	    yield scrapy.Request(href.extract(), callback=self.parse_links)
	else:
	  print "\nERROR: No jobs found at " + url     
   
   def parse_links(self, response):
      # NOTE: this only works for one company.  Deloitte, for example, uses divs instead of ul/li
      #print response.xpath('//div[@id="jobdescSec"]/ul/li/text()')
      
      item = headhunterItem()
      item['org'] = response.xpath('//ul/li[@class="employer"]/a/text()').extract()
      item['title'] = response.selector.xpath('//title/text()').extract()
      item['url'] = response.url
      #for sel in response.xpath('//div[@id="jobdescSec"]/*/text()'):
      item['req'] = response.xpath('//div[@id="jobdescSec"]/*/text()').extract()
      yield item
  