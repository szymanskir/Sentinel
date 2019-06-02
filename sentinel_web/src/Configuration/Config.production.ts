declare var app_config: {
    readonly API_ENDPOINT: string;
    readonly AWS_REGION: string;
    readonly COGNITO_USER_POOL_ID: string;
    readonly COGNITO_WEB_CLIENT_ID: string;
};

const config: Configuration = {
    apiEndpoint: app_config.API_ENDPOINT,
    awsRegion: app_config.AWS_REGION,
    cognitoUserPoolId: app_config.COGNITO_USER_POOL_ID,
    cognitoWebClientId: app_config.COGNITO_WEB_CLIENT_ID
};

export default config;
