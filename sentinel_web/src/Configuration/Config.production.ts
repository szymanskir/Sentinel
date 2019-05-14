declare var app_config: {
    readonly API_ENDPOINT: string;
};

const config: Configuration = {
    apiEndpoint: app_config.API_ENDPOINT,
};

export default config;
