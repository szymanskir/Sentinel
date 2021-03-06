import * as moment from "moment";
import { Mention } from "./Models/Mention";
import config from "config";
import { Auth } from "aws-amplify";


const baseAddress = config.apiEndpoint;

class ApiClient {

    async addKeyword(keyword: string) {
        const params = new URLSearchParams({
            keyword: keyword
        });

        const request = await this.prepareRequest(`/keywords/add?${params}`);
        const response = await fetch(request);
    }

    async updateKeyword(oldKeyword: string, currentKeyword: string) {
        const params = new URLSearchParams({
            old_keyword: oldKeyword,
            current_keyword: currentKeyword
        });

        const request = await this.prepareRequest(`/keywords/update?${params}`);
        const response = await fetch(request);
    }

    async deleteKeyword(keyword: string) {
        const params = new URLSearchParams({
            keyword: keyword
        });

        const request = await this.prepareRequest(`/keywords/delete?${params}`);
        const response = await fetch(request);
    }

    async getMentionsCount(from: moment.Moment, to: moment.Moment, keywords: string[]) {
        const params = new URLSearchParams({
            from: from.toISOString(),
            to: to.toISOString(),
        });

        for (let word of keywords) {
            params.append("keywords", word);
        }

        const request = await this.prepareRequest(`/mentions-count?${params}`);
        const response = await fetch(request);
        const json = await response.json();
        return json;
    }

    async getMentions(from: moment.Moment, to: moment.Moment, keywords: string[]) {
        const params = new URLSearchParams({
            from: from.toISOString(),
            to: to.toISOString(),
        });

        for (let word of keywords) {
            params.append("keywords", word);
        }

        const request = await this.prepareRequest(`/mentions?${params}`);
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

        const request = await this.prepareRequest(`/sentiment?${params}`);
        const response = await fetch(request);
        const json = await response.json();
        return json;
    }

    async getAllKeywords() {
        const request = await this.prepareRequest("/my-keywords");
        const response = await fetch(request);
        const json = await response.json();
        return json as string[];
    }

    private async prepareRequest(path: string) {
        const request = new Request(`${baseAddress}${path}`);
        const token = await this.getToken();
        request.headers.append("Authorization", `Bearer ${token}`);
        return request;
    }

    private async getToken() {
        let session = await Auth.currentSession();
        return session.getAccessToken().getJwtToken();
    }
}

export const apiClient = new ApiClient();
