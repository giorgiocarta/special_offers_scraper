build:
	docker build . --tag giorgiocarta/shopping_offers_scraper:0.1

run:
	docker run -it --rm giorgiocarta/shopping_offers_scraper:0.1

push:
	docker push giorgiocarta/shopping_offers_scraper:0.1