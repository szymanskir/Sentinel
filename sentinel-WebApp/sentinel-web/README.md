## Develop
Install node, npm and yarn.
Run:
```
yarn install
yarn dev
```

If you receive 'Error: EMFILE: too many open files' error, it means that watch cannot reserve
enough file desciptors. The app will work, but you won't have hot-reloading. To increase allowed number of FDs run `ulimit -n LARGE_POWER_OF_TWO` (resets after restart), or check 
how to do it permanently on your system.

## Build
`yarn build` builds an app bundle. You also need to pass `config.js` file containing configuration options to the root of bundle.
Config file should looks like this
```
var app_config = {
    "CONFIG_KEY": "CONFIG_VALUE"
}
```
All neccesary variables are defined in src/Configuration/Config.production.ts file
