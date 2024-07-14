# import scrapy
# import re


# def extract_category(url):
#     category = url.split("/")[-1]
#     category = category.replace("-", " ")
#     category = re.sub(r"\d+$", "", category)
#     return category


# class SpiceMasterSpider(scrapy.Spider):
#     name = "spicemaster"
#     allowed_domains = ["wolt.com"]
#     start_urls = ["https://wolt.com/en/deu/munich/venue/spicemaster"]

#     def parse(self, response):
#         # Extract all category links from the main page
#         category_links = response.xpath(
#             '//a[contains(@href, "/items/")]/@href'
#         ).getall()
#         for link in category_links:
#             yield response.follow(link, self.parse_category)

#     def parse_category(self, response):
#         # Extract category from URL
#         category = extract_category(response.url)

#         # Extract item cards directly from the category page
#         rows = response.xpath('//div[@data-test-id="ItemCard"]')

#         for row in rows:
#             item_name_parts = row.xpath(
#                 './/h3[@data-test-id="ImageCentricProductCard.Title"]//text()'
#             ).getall()
#             item_price_parts = row.xpath(
#                 './/div[@data-test-id="ImageCentricProductCardPrice"]//text()'
#             ).getall()

#             item_name = " ".join(item_name_parts).strip() if item_name_parts else "N/A"
#             item_price = (
#                 " ".join(item_price_parts).strip() if item_price_parts else "N/A"
#             )

#             yield {
#                 "category": category,
#                 "item_name": item_name,
#                 "item_price": item_price,
#             }

#         # Follow pagination links if they exist
#         next_page = response.xpath(
#             '//a[contains(@class, "Pagination_next")]/@href'
#         ).get()
#         if next_page:
#             yield response.follow(next_page, self.parse_category)
