import * as React from "react";
import Grid from "@material-ui/core/Grid";
import { CardContent, Card, Typography, CardHeader, IconButton, List, Button, Divider } from "@material-ui/core";
import AddIcon from "@material-ui/icons/Add";
import KeywordListItem from "./KeywordListItem";
import { KeywordItem } from "../Models/KeywordItem";
import { apiClient } from "../ApiClient";
import AddKeywordDialog from "./AddKeywordDialog";

export interface KeywordsTabItemProps {

}

export interface KeywordsTabItemState {
    keywords: KeywordItem[];
    isDialogOpen: boolean;
}

class KeywordsTabItem extends React.Component<KeywordsTabItemProps, KeywordsTabItemState> {
    constructor(props: KeywordsTabItemProps) {
        super(props);
        this.state = {
            keywords: [],
            isDialogOpen: false
        };
    }

    componentDidMount() {
        this.downloadKeywords();
    }

    private createStartEditCallback(index: number): () => void {
        return () => {
            const keywords = Object.assign([], this.state.keywords) as KeywordItem[];
            keywords.forEach(k => k.isEditable = false);
            keywords[index].isEditable = true;
            this.setState({
                keywords
            });
        };
    }

    private createEndEditCallback(index: number): (oldKeyword: string, currentKeyword: string) => void {
        return async (oldKeyword: string, currentKeyword: string) => {
            await apiClient.updateKeyword(oldKeyword, currentKeyword);
            this.downloadKeywords();
        };
    }

    private createOnDeleteCallback(index: number): () => void {
        return async () => {
            const keyword = this.state.keywords[index].keyword;
            await apiClient.deleteKeyword(keyword);
            this.downloadKeywords();
        };
    }

    private openAddKeywordDialog() {
        this.setState({
            isDialogOpen: true
        });
    }

    private closeAddKeywordDialog() {
        this.setState({
            isDialogOpen: false
        });
    }

    private async addKeyword(keywordName: string) {
        await apiClient.addKeyword(keywordName);
        this.downloadKeywords();
    }

    render() {
        return <div className="flex-grow-1">
            <AddKeywordDialog isOpen={this.state.isDialogOpen} onCancel={() => this.closeAddKeywordDialog()} onSubmit={(keywordName: string) => { this.addKeyword(keywordName); this.closeAddKeywordDialog(); }} />
            <Grid container spacing={8} justify="center">
                <Grid item xs={4}>
                    <Card>
                        <CardHeader title="Keywords" action={<Button onClick={() => this.openAddKeywordDialog()}><AddIcon /> Add keyword </Button>} />
                        <CardContent>
                            <List>
                                {this.state.keywords.map((keyword, index) => <KeywordListItem key={index}
                                    name={keyword.keyword}
                                    isEditable={this.state.keywords[index].isEditable}
                                    onStartEditCallback={this.createStartEditCallback(index)}
                                    onEndEditCallback={this.createEndEditCallback(index)}
                                    onDelete={this.createOnDeleteCallback(index)} />)}
                            </List>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </div>;
    }

    private downloadKeywords = async () => {
        const keywords = await apiClient.getAllKeywords();
        this.setState({ keywords: keywords.map(keyword => new KeywordItem(keyword, false)) });
    }
}

export default KeywordsTabItem;
