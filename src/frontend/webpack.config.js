const path = require('path');

module.exports = {
    entry: {
        "kusari": path.resolve(__dirname, "./src/js/main.js"),
    },
    devtool: 'source-map',
    module: {
        rules: [
          {
            test: /\.(js|jsx)$/,
            exclude: /node_modules/,
            use: {
              loader: "babel-loader",
            }
          },
          {
            test: /\.s[ac]ss$/i,
            use: [
              // Creates `style` nodes from JS strings
              'style-loader',
              // Translates CSS into CommonJS
              'css-loader',
              // Compiles Sass to CSS
              'sass-loader',
            ],
          },
        ]
      },
      resolve: {
        extensions: ['*', '.js', '.scss', '.css', '.jsx']
      },
    output: {
        path: path.resolve(__dirname, "./src/dist"),
        filename: "[name]-bundle.js"
    }
};
