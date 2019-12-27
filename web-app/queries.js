var promise = require('bluebird');
var options = {
  // Initialization Options
  promiseLib: promise
};
var pgp = require('pg-promise')(options);
var db = pgp('postgres://bookopedia:bookopedia@bookopedia_postgres/bookopedia');

function getAllBooks(req, res, next) {
  db.any('select book.id as book_id, book.title as title, category.title as category, thumbnail, rating, price, currency, availability from book join category on book.category=category.id')
    .then(function (data) {
      res.status(200)
        .json(data);
    })
    .catch(function (err) {
      return next(err);
    });
}

// add query functions
module.exports = {
  getAllBooks: getAllBooks,
};
