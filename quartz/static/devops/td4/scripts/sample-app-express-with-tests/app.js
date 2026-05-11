const express = require('express');

const app = express();

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
  res.send('Hello, World!');
});

app.get('/name/:name', (req, res) => {

  res.render('hello', {name: req.params.name});
});

app.get('/add/:a/:b', (req, res) => {
  const a = parseFloat(req.params.a);
  const b = parseFloat(req.params.b);
  
  if (isNaN(a) || isNaN(b)) {
    return res.status(400).send('Invalid numbers');
  }
  
  const sum = a + b;
  res.send(`${a} + ${b} = ${sum}`);
});

module.exports = app;
