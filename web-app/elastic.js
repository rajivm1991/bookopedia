var elasticsearch = require('elasticsearch');
var client = new elasticsearch.Client({
  host: 'localhost:9200',
  log: 'trace',
  apiVersion: '7.2', // use the same version of your Elasticsearch instance
});


function searchBooks(title) {
    return client.search({
      index: 'books',
      body: {
        query: {
          match: {
            title: title
          }
        }
      }
    })
}

// add query functions
module.exports = {
  searchBooks: searchBooks,
};
