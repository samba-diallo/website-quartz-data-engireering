const request = require('supertest');
const app = require('./app');                             

describe('Test the app', () => {                          

  test('Get / should return Hello, World!', async () => { 
    const response = await request(app).get('/');         
    expect(response.statusCode).toBe(200);                
    expect(response.text).toBe('Hello, World!');          
  });

  test('Get /name/Bob should return Hello, Bob!', async () => {
    const response = await request(app).get('/name/Bob');
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe('Hello, Bob!');
  });

  const maliciousUrl = '/name/%3Cscript%3Ealert("hi")%3C%2Fscript%3E';
  const sanitizedHtml = 'Hello, &lt;script&gt;alert(&#34;hi&#34;)&lt;/script&gt;!'

  test('Get /name should sanitize its input', async () => {
    const response = await request(app).get(maliciousUrl);
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe(sanitizedHtml);
  });

});

describe('Test the /add endpoint', () => {

  test('Get /add/2/3 should return 5', async () => {
    const response = await request(app).get('/add/2/3');
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe('2 + 3 = 5');
  });

  test('Get /add/10/20 should return 30', async () => {
    const response = await request(app).get('/add/10/20');
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe('10 + 20 = 30');
  });

  test('Get /add/5.5/4.5 should handle decimals', async () => {
    const response = await request(app).get('/add/5.5/4.5');
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe('5.5 + 4.5 = 10');
  });

  test('Get /add/abc/def should return 400 for invalid numbers', async () => {
    const response = await request(app).get('/add/abc/def');
    expect(response.statusCode).toBe(400);
    expect(response.text).toBe('Invalid numbers');
  });

});
