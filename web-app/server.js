'use strict';

const express = require('express');
const router = express.Router();
const db = require('./queries')
const es = require('./elastic')

// Constants
const PORT = 5000;
const HOST = '0.0.0.0';

// App
const app = express();

router.get('/books', db.getAllBooks);
router.get('/books/search', function (req, res, next) {
  es.searchBooks(req.param('title')).then(function (result) { res.json(result.hits.hits) });
});

/** /
// An api endpoint that returns a short list of items
app.get('/api/getList', (req,res) => {
    var list = ["item1", "item2", "item3"];
    res.json(list);
    console.log('Sent list of items');
});
app.get('/api/books/:category', (req,res) => {
    var list = ["book1", "book2", "book3"];
    res.json(list);
    console.log(`Sent list of books://${req.params.category}`);
});

// Handles any requests that don't match the ones above
app.get('*', (req,res) =>{
    res.send('There is nothing here!')
});
/**/

app.use('/api', router)
app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);
