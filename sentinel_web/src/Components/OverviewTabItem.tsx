import * as React from "react";
import * as moment from "moment";
import { AppBar, Toolbar, Typography, IconButton, Grid, Button, Card, CardContent, Checkbox, FormControlLabel } from "@material-ui/core";
import { apiClient } from "../ApiClient";
import MenuIcon from "@material-ui/icons/Menu";
import DashboardPlot from "./DashboardPlot";
import DashboardParamsSelector from "./DashboardParamsSelector";
import CommentsTable from "./CommentsTable";


interface OverviewTabItemState {
    isDrawerOpen: boolean;
    allKeywords: string[];
    selectedKeywords: string[];
    from: moment.Moment;
    to: moment.Moment;
    mentions: [];
    mentionsCount: [];
    sentiments: [];
    refreshIntervalId: any;
    isLiveModeOn: boolean;
}

export class OverviewTabItem extends React.Component<{}, OverviewTabItemState> {
    constructor(props: {}) {
        super(props);
        this.state = {
            isDrawerOpen: false,
            allKeywords: [],
            selectedKeywords: [],
            mentions: [],
            mentionsCount: [],
            sentiments: [],
            from: moment().add(-7, "days").startOf("day"),
            to: moment().add(1, "days").startOf("day"),
            refreshIntervalId: null,
            isLiveModeOn: false
        };

    }

    componentDidMount() {
        this.downloadKeywords();
    }

    private startLiveMode() {
        let liveModeId = setInterval(() => { this.downloadMentions(); this.downloadKeywords(); }, 5000);
        this.setState({
            refreshIntervalId: liveModeId,
            isLiveModeOn: true
        });
    }

    private stopLiveMode() {
        clearInterval(this.state.refreshIntervalId);
        this.setState({
            isLiveModeOn: false
        });
    }


    render() {
        return <div className="flex-grow-1">
            <Grid container spacing={8} direction="column" alignItems="center">
                <Grid container item xs={12} spacing={8} >
                    <Grid container item spacing={8} xs={5} direction="column">
                        <Grid item>
                            <Card>
                                <CardContent>
                                    <Typography variant="h5" component="h6">
                                        Settings
                                </Typography>
                                    <DashboardParamsSelector
                                        allKeywords={this.state.allKeywords}
                                        selectedKeywords={this.state.selectedKeywords}
                                        from={this.state.from}
                                        to={this.state.to}
                                        onSelectedKeywordsChanged={selectedKeywords => this.setState({ selectedKeywords })}
                                        onFromChanged={from => this.setState({ from })}
                                        onToChanged={to => this.setState({ to })}
                                    />
                                    <Button
                                        variant="contained"
                                        onClick={this.downloadMentions}
                                        color="primary">
                                        Fetch
                                    </Button>
                                    <FormControlLabel label={"Live Mode"} control={<Checkbox checked={this.state.isLiveModeOn} onChange={(event: any, value: boolean) => value ? this.startLiveMode() : this.stopLiveMode()} />} />
                                </CardContent>
                            </Card>
                        </Grid>
                        <Grid container item direction="column">
                            <CommentsTable mentions={this.state.mentions} />
                        </Grid>
                    </Grid>
                    <Grid container item spacing={8} xs={7} direction="column">
                        <Grid item>
                            <DashboardPlot title="Sentiment plot" plotData={this.state.sentiments} />
                        </Grid>
                        <Grid item>
                            <DashboardPlot title="Mentions count" plotData={this.state.mentionsCount} />
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </div>;
    }

    private downloadKeywords = async () => {
        const keywords = await apiClient.getAllKeywords();
        this.setState({ allKeywords: keywords });
    }

    private downloadMentions = async () => {
        const mentionsCountPromise = apiClient.getMentionsCount(
            this.state.from,
            this.state.to,
            this.state.selectedKeywords
        );

        const sentimentsPromise = apiClient.getMentionsSentimentScores(
            this.state.from,
            this.state.to,
            this.state.selectedKeywords
        );

        const mentionsPromise = apiClient.getMentions(
            this.state.from,
            this.state.to,
            this.state.selectedKeywords
        );

        const mentions = await mentionsPromise;
        const mentionsCount = await mentionsCountPromise;
        const sentiments = await sentimentsPromise;

        this.setState({ mentions, sentiments, mentionsCount });
    }
}
