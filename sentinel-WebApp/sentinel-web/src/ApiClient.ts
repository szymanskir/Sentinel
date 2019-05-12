import * as moment from "moment";
import { Mention } from "./Models/Mention";
import config from "config";

const baseAddress = config.apiEndpoint;

class ApiClient {

    async getMentionsCount(from: moment.Moment, to: moment.Moment, keywords: string[]) {
        const params = new URLSearchParams({
            from: from.toISOString(),
            to: to.toISOString(),
        });

        for (let word of keywords) {
            params.append("keywords", word);
        }

        const request = new Request(`${baseAddress}/mentions?${params}`);
        const response = await fetch(request);
        const json = await response.json();
        return json;
    }

    async getMentionsSentimentScores(from: moment.Moment, to: moment.Moment, keywords: string[]) {
        const params = new URLSearchParams({
            from: from.toISOString(),
            to: to.toISOString(),
        });

        for (let word of keywords) {
            params.append("keywords", word);
        }

        const request = new Request(`${baseAddress}/sentiment?${params}`);
        const response = await fetch(request);
        const json = await response.json();
        return json;
    }

    async getAllKeywords() {
        const request = new Request(`${baseAddress}/my-keywords`);
        const response = await fetch(request);
        const json = await response.json();
        return json as string[];
    }
}

export const apiClient = new ApiClient();
