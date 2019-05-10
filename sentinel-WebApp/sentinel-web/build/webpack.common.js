const webpack = require("webpack");
const path = require("path");
const paths = require("./paths");

const HtmlWebpackPlugin = require("html-webpack-plugin");
const ForkTsCheckerPlugin = require("fork-ts-checker-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");

const tsconfig = require("../tsconfig");
const deployDir = process.env.DEPLOY_DIR || path.resolve(__dirname, "deploy");

const mappings = {};

for (let key in tsconfig.compilerOptions.paths) {
    const v = tsconfig.compilerOptions.paths[key][0];
    const from = key.substr(0, key.length - 2);
    const to = v.substr(0, v.length - 2);

    mappings[from] = path.join(__dirname, "..", to);
}

module.exports = {
    entry: [
        path.join(paths.src, "index.tsx")
    ],

    plugins: [
        new HtmlWebpackPlugin({
            template: path.join(paths.public, "index.html"),
        }),
        new webpack.EnvironmentPlugin({
            "APP_VERSION": "0.0.0-dev"
        }),
        new CopyWebpackPlugin([{
            from: path.join(paths.public, "favicon.ico")
        }]),
        new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
        new ForkTsCheckerPlugin({
            checkSyntacticErrors: true,
            tsconfig: paths.tsConfig,
            tslint: paths.tsLint,
            watch: [paths.src],
            async: false,
        })
    ],

    output: {
        path: path.resolve(deployDir),
        filename: "[name].js",
        publicPath: "/",
        pathinfo: false
    },

    resolve: {
        extensions: [".ts", ".tsx", ".js"],
        alias: {
            ...mappings,
        }
    },

    optimization: {
        splitChunks: {
            chunks: "all"
        }
    },

    module: {
        rules: [{
            test: /\.tsx?$/,
            loader: 'babel-loader',
            include: [
                paths.src
            ],
            options: {
                babelrc: false,
                sourceMaps: true,
                presets: ["@babel/react", "@babel/typescript", ["@babel/env", { modules: false, useBuiltIns: "usage" }]],
                plugins: [
                    "emotion",
                    "@babel/plugin-syntax-dynamic-import",
                    ["@babel/plugin-proposal-class-properties", { "loose": false }],
                ]
            }
        },
        {
            test: /\.(ttf|eot)(\?[\s\S]+)?$/,
            loader: "file-loader",
            options: {
                name: "fonts/[name].[ext]"
            }
        },
        {
            test: /\.(jpg|png|svg|gif)$/,
            loader: "file-loader",
            options: {
                name: "images/[name]-[hash:5].[ext]"
            }
        }
        ]
    }
};
