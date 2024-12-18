from src.crawler.crawler import brandCrawler, laptopCrawler

if __name__ == "__main__":
    # brandCrawler = brandCrawler(brand_path='data/brand_html', config='config/fpt.json')
    # brandCrawler.crawl()
    laptopCrawler = laptopCrawler("data/data.csv","data/laptop_html")
    laptopCrawler.crawl("data/data.csv")