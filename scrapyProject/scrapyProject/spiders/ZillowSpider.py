import scrapy
from scrapyProject.items import ScrapyprojectItem

class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    zipCode = [
        94002, 94005, 94010, 94014, 94015, 94019, 94020, 94021, 94025, 94027, 94028, 94030, 94037, 94038, 94044, 94060,
        94061, 94062, 94063,94065, 94066, 94070, 94074, 94080, 94102, 94103, 94104, 94105, 94107, 94108, 94109, 94110,
        94111, 94112, 94114,94115, 94116, 94117,94118, 94121, 94122, 94123, 94124, 94127, 94128, 94129, 94130, 94131,
        94132, 94133, 94134, 94158, 94401, 94402,94403, 94404, 94501,94502, 94505, 94506, 94507, 94509, 94511, 94513,
        94514, 94516, 94517, 94518, 94519, 94520, 94521, 94523, 94525,94526, 94528, 94530,94531, 94536, 94538, 94539,
        94541, 94542, 94544, 94545, 94546, 94547, 94548, 94549, 94550, 94551, 94552, 94553,94555, 94556, 94560,94561,
        94563, 94564, 94565, 94566, 94568, 94569, 94572, 94575, 94577, 94578, 94582, 94583, 94586, 94587, 94588,94595,
        94596, 94597,94598, 94601, 94602, 94603, 94605, 94606, 94607, 94608, 94609, 94610, 94611, 94612, 94613, 94618,
        94619, 94621,94702, 94703, 94704,94705, 94706, 94707, 94708, 94709, 94710, 94720, 94801, 94803, 94804, 94805,
        94806, 94850, 94901, 94903, 94904,94920, 94924, 94925,94929, 94930, 94933, 94937, 94938, 94939, 94940, 94941,
        94945, 94946, 94947, 94949, 94950, 94956, 94957, 94960,94963, 94964, 94965,94970, 94971, 94973
    ]

    base_url_part1 = 'https://www.zillow.com/homes/'
    base_url_part2 = '_rb/'
    url_list = []
    for code in zipCode:
        url = base_url_part1 + str(code) + base_url_part2
        url_list.append(url)

    start_urls = url_list


    def parse(self, response):

        for house in response.xpath('.//div[@class="list-card-info"]/a/@href'):
            yield scrapy.Request(
                response.urljoin(house.extract()),
                callback=self.parse_page
            )

        next_page = response.xpath('.//a[@title="Next page"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

    def parse_page(self, response):
        item = ScrapyprojectItem()

        item['price'] = response.xpath('.//div[@class="ds-summary-row"]//span/text()').extract_first()
        item['type'] = response.xpath('.//ul[@class="ds-home-fact-list"]/li[1]/span[2]/text()').extract_first()
        item['year'] = response.xpath('.//ul[@class="ds-home-fact-list"]/li[2]/span[2]/text()').extract_first()
        item['lot_size'] = response.xpath('.//ul[@class="ds-home-fact-list"]/li[last()-1]/span[2]/text()').extract_first()
        item['price_per_sqft'] = response.xpath('.//ul[@class="ds-home-fact-list"]/li[last()]/span[2]/text()').extract_first()
        item['street'] = response.xpath('.//div[@class="ds-home-details-chip"]/div[2]//header//span[1]/text()').extract_first()
        item['city_state'] = response.xpath('.//div[@class="ds-home-details-chip"]/div[2]//header//span[2]/text()[2]').extract_first()
        item['bedrooms'] = response.xpath('.//h3[@class="ds-bed-bath-living-area-container"]/span[1]/span/text()').extract_first()
        item['size'] = response.xpath('//h3[@class="ds-bed-bath-living-area-container"]/span[last()]/span[1]/text()').extract_first()
        item['bathrooms'] = response.xpath('.//h3[@class="ds-bed-bath-living-area-container"]//*[3]//span/text()').extract_first()
        item['time_on_zillow'] = response.xpath('.//div[@class="ds-overview"]//div[@class="sc-oVdHe bsLHzL"][1]/div[2]/text()').extract_first()
        item['views'] = response.xpath('.//div[@class="ds-overview"]//div[@class="sc-oVdHe bsLHzL"][2]/div[2]/text()').extract_first()
        item['saves'] = response.xpath('.//div[@class="ds-overview"]//div[@class="sc-oVdHe bsLHzL"][3]/div[2]/text()').extract_first()
        item['neighborhood'] = response.xpath('.//span[@id="skip-link-neighborhood"]/following-sibling::div/h4/text()').extract_first()


        yield item
