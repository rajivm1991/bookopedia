Bookopedia
==========

**To bring postgress and elasticsearch up**
 
`docker-compose up -d bookopedia_postgres bookopedia_es`

**To run express.js REST api server**

```bash
cd web-app
npm start
```

**To run ReactJS app**


```bash
cd web-app/client
npm start
```

**To scrape & index books**


* create tables in postgress
* scrapes books and stores in postgres
* indexes books in elasticsearch

```bash
cd data-mgmt
./migrate
python -m scraper.scrape-books
python -m index.index-books
```