import scrapy

class JobItem(scrapy.Item):
    job_title = scrapy.Field()
    company_name = scrapy.Field()
    location = scrapy.Field()
    job_type = scrapy.Field()
    job_description = scrapy.Field()
    email = scrapy.Field()
    application_link = scrapy.Field()