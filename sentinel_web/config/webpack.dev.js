const webpack = require("webpack");
const paths = require("./paths");
const merge = require("webpack-merge");

const CommonConfig = require("./webpack.common.js");

module.exports = merge(CommonConfig, {
    entry: [
        "webpack-dev-server/client?http://localhost:3000",
        "webpack/hot/only-dev-server"
    ],

    devtool: "source-map",

    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NamedModulesPlugin(),
        new webpack.NoEmitOnErrorsPlugin(),

        new webpack.DefinePlugin({
            "process.env": {
                APP_VERSION: JSON.stringify("development"),
            },
        }),
    ],

    resolve: {
        alias: {
            "config": paths.config("dev")
        }
    },

    devServer: {
        hot: true,
        publicPath: "/",
        disableHostCheck: true,
        public: "http://localhost:3000",
        port: 3000,
        host: "0.0.0.0",
        historyApiFallback: true,
    }
});
