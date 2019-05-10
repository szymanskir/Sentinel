import * as moment from "moment";
import { Mention } from "./Models/Mention";
import config from "config";

const baseAddress = config.apiEndpoint;

class ApiClient {

    async getMentions(from: moment.Moment, to: moment.Moment, keywords: string[]) {
        const params = new URLSearchParams({
            from: from.toISOString(true),
            to: to.toISOString(true),
        });

        for (let word of keywords) {
            params.append("keywords", word);
        }

        const request = new Request(`${baseAddress}/mentions?${params}`);
        const response = await fetch(request);
        const json = await response.json();
        return json as Mention[];
    }

    async getAllKeywords() {
        const request = new Request(`${baseAddress}/my-keywords`);
        const response = await fetch(request);
        const json = await response.json();
        return json as string[];
    }
}

export const apiClient = new ApiClient();
