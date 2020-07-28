const path = require("path");
const dist = path.resolve(__dirname, "dist");

//const CopyPlugin = require("copy-webpack-plugin");
//const WasmPackPlugin = require("@wasm-tool/wasm-pack-plugin");


module.exports = {
    devServer: {
        contentBase: dist,
        useLocalIp: true,
        sockHost: "10.0.42.19",
        https: true,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        },
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                pathRewrite: { 'api': 'images' }
            },
            '/arts': {
                target: 'http://localhost:8000',
                pathRewrite: function(path, req) {
                    console.log(path)
                    return path
                }
            } 
        }
    },
    // publicPath: '/static/',
    /*chainWebpack: config => {
        config
            .plugin('wasmpack')
            .use(WasmPackPlugin, [
                {
                    crateDirectory: __dirname,
                    //extraArgs: "--out-name index"
                }]);
        config
            .plugin('copy')
            .use(CopyPlugin, [[path.resolve(__dirname, "public")]]);
        //config
        //    .plugin('workspace')
        
    },*/

}