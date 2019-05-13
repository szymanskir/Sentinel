const path = require("path");

const configRoot = __dirname;
const appRoot = path.resolve(configRoot, "..");

const src = path.join(appRoot, "src");
const tsConfig = path.join(appRoot, "tsconfig.json");
const nodeModules = path.join(appRoot, "node_modules");
const public = path.join(appRoot, "public");

const tsLint = path.join(appRoot, "tslint.json");

module.exports = {
    appRoot,
    src,
    tsConfig,
    tsLint,
    nodeModules,
    public,
    config: env => path.join(src, "Configuration", `Config.${env}.ts`)
}
