import scrapy
import re


def extract_category(url, index):
    category = url.split("/")[index]
    category = category.replace("-", " ")
    category = re.sub(r"\d+$", "", category)
    return category


class PennySpider(scrapy.Spider):
    name = "penny"
    allowed_domains = ["wolt.com"]
    start_urls = [
        # "https://wolt.com/en/deu/munich/venue/penny-neuhausen",
        "https://wolt.com/en/deu/munich/venue/flink-barthstr",
        "https://wolt.com/en/deu/munich/venue/flink-blutenburgstr/",
        "https://wolt.com/en/deu/munich/venue/flink-ungererstr",
        # "https://wolt.com/en/deu/munich/venue/edeka-theresie",
        # "https://wolt.com/en/deu/munich/venue/sri-balaji-indian-market-mnchen",
    ]

    def parse(self, response):
        main_category_links = response.xpath(
            '//a[@data-test-id="navigation-bar-link"]/@href'
        ).getall()

        for link in main_category_links:
            yield response.follow(
                link,
                self.parse_main_category,
                meta={"main_category_name": link},
            )

    def parse_main_category(self, response):
        main_category_links = response.meta["main_category_name"]
        sub_category = response.xpath('//a[contains(@href, "/items/")]/@href').getall()
        for link in sub_category:
            yield response.follow(
                link,
                self.parse_items,
                meta={"main_category_name": main_category_links},
            )

    def parse_items(self, response):
        main_category = response.meta["main_category_name"]
        rows = response.xpath('//div[@data-test-id="ItemCard"]')

        for row in rows:
            item_name_parts = row.xpath(
                './/h3[@data-test-id="ImageCentricProductCard.Title"]//text()'
            ).get()
            item_price_parts = row.xpath(
                './/div[@data-test-id="ImageCentricProductCardPrice"]//text()'
            ).get()
            item_info_parts = row.xpath(
                './/div[@data-test-id="ImageCentricProductCardPrice"]/following-sibling::div[2]//span[@data-test-id="ImageCentricProductCardProductInfo"]//text()'
            ).get()
            item_unit_parts = row.xpath(
                '//div[@data-test-id="ImageCentricProductCardPrice"]/following-sibling::div[2]//span[@data-test-id="ImageCentricProductCardUnitPrice"]//text()'
            ).get()
            link = row.xpath('.//a[@data-test-id="CardLinkButton"]/@href').get()

            yield {
                "storename": extract_category(main_category, -3),
                "main_category": extract_category(main_category, -1),
                "sub_category": extract_category(response.url, -1),
                "item_name": item_name_parts,
                "item_price": item_price_parts,
                "item_info": item_info_parts,
                "item_unit": item_unit_parts,
                "link": "https://wolt.com" + link,
            }
