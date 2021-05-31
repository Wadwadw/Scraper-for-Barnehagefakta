import scrapy
import xml.etree.ElementTree as ET
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class FirstSpider(scrapy.Spider):
    name = 'first'
    allowed_domains = [
        'sok.udir.no',
        'www.barnehagefakta.no',
    ]

    def __init__(self):
        self.n = 20

    def start_requests(self):
        yield scrapy.Request(
            url=f'https://sok.udir.no/_api/search/query?selectproperties=%27Title%2CBarnehagefaktaOrgnummer%2CBarnehagefaktaFylkesnavn%2CBarnehagefaktaKommunenavn%2CBarnehagefaktaBesoksAdresseAdresselinje%2CBarnehagefaktaBesoksAdressePoststed%2CBarnehagefaktaBesoksAdressePostnummer%2CBarnehagefaktaEierform%2CBarnehagefaktaAntallBarn%2CBarnehagefaktaAlder%2CBarnehagefaktaKoordinatLatDecimal%2CBarnehagefaktaKoordinatLngDecimal%27&refiners=%27BarnehagefaktaFylkesnummerOgFylkesnavn%2CBarnehagefaktaFylkesnummerOgKommunenavn(filter%3D1000%2F1%2F*)%2CBarnehagefaktaEierform%2CBarnehagefaktaPedagogiskProfil%2CBarnehagefaktaBarnehageType%2CBarnehagefaktaAlder%2CBarnehagefaktaAntallBarnInteger(discretize%3Dmanual%2F26%2F51%2F76%2F101)%27&properties=%27SourceName%3ABarnehagefakta%2CSourceLevel%3ASPSite%27&startrow=0&rowlimit=20&clienttype=%27AllResultsQuery%27&culture=1044&trimduplicates=false&sortlist=%27Rank%3Adescending%27&querytext=%27*%27&QueryTemplatePropertiesUrl=%27spfile://webroot/queryparametertemplate-Barnehagefakta.xml%27',
            callback=self.parse_id
        )

    def parse_id(self, response):
        tree = ET.fromstring(response.text)
        prefix_map = {'d': 'http://schemas.microsoft.com/ado/2007/08/dataservices'}
        root = tree.findall('.//d:Table/d:Rows/d:element/d:Cells', prefix_map)
        total = tree.find('.//d:TotalRows', prefix_map).text
        for ro in root:
            value = ro.find('.//d:element[4]/d:Value', prefix_map).text
            value_name = ro.find('.//d:element[3]/d:Value', prefix_map).text
            value_name_ex = ''
            for i in value_name:
                if i == ' ':
                    i = '-'
                value_name_ex += i

            yield SeleniumRequest(url=f'https://www.barnehagefakta.no/barnehage/{value}/{value_name_ex}',
                                  wait_time=5,
                                  wait_until=EC.element_to_be_clickable((By.XPATH, "(//a[@class='ng-binding'])[2]")),
                                  callback=self.parse_item
                                  )
        if self.n < int(total):
            self.n += 20
            yield scrapy.Request(
                url=f'https://sok.udir.no/_api/search/query?selectproperties=%27Title%2CBarnehagefaktaOrgnummer%2CBarnehagefaktaFylkesnavn%2CBarnehagefaktaKommunenavn%2CBarnehagefaktaBesoksAdresseAdresselinje%2CBarnehagefaktaBesoksAdressePoststed%2CBarnehagefaktaBesoksAdressePostnummer%2CBarnehagefaktaEierform%2CBarnehagefaktaAntallBarn%2CBarnehagefaktaAlder%2CBarnehagefaktaKoordinatLatDecimal%2CBarnehagefaktaKoordinatLngDecimal%27&refiners=%27BarnehagefaktaFylkesnummerOgFylkesnavn%2CBarnehagefaktaFylkesnummerOgKommunenavn(filter%3D1000%2F1%2F*)%2CBarnehagefaktaEierform%2CBarnehagefaktaPedagogiskProfil%2CBarnehagefaktaBarnehageType%2CBarnehagefaktaAlder%2CBarnehagefaktaAntallBarnInteger(discretize%3Dmanual%2F26%2F51%2F76%2F101)%27&properties=%27SourceName%3ABarnehagefakta%2CSourceLevel%3ASPSite%27&startrow={self.n}&rowlimit=20&clienttype=%27AllResultsQuery%27&culture=1044&trimduplicates=false&sortlist=%27Rank%3Adescending%27&querytext=%27*%27&QueryTemplatePropertiesUrl=%27spfile://webroot/queryparametertemplate-Barnehagefakta.xml%27',
                callback=self.parse_id,
            )

    def parse_item(self, response):
        yield {
            "Company name": response.xpath("//div/div/h1/text()").get(),
            "E-mail": response.xpath("(//a[@class='ng-binding'])[2]/@href").get(),
            "number": response.xpath("((//div[@class='row']/section/div/section/ul/li)[3]/span)[2]/text()").get(),
            "link": response.url,
        }

