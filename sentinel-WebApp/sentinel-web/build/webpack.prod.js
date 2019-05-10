const paths = require("./paths");
const merge = require("webpack-merge");

const HtmlWebpackIncludeAssetsPlugin = require("html-webpack-include-assets-plugin");
const CommonConfig = require("./webpack.common.js");

module.exports = merge(CommonConfig, {
    plugins: [
        new HtmlWebpackIncludeAssetsPlugin({
            assets: ["config.js"],
            append: false
        })
    ],

    resolve: {
        alias: {
            "config": paths.config("production")
        }
    }
});
