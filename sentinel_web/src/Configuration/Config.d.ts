interface Configuration {
    apiEndpoint: string;
    awsRegion: string;
    cognitoUserPoolId: string;
    cognitoWebClientId: string;
}

declare module "config" {
    const config: Configuration;

    export default config;
}
