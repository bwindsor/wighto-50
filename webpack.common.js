const path = require('path');

module.exports = {
  entry: {
    app: './js/app.v2.js',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    clean: true,
    filename: './js/app.v2.js',
  },
};
