import * as React from "react";
import * as moment from "moment";
import { AppBar, Toolbar, Typography, IconButton, Grid, Button, Card, CardContent } from "@material-ui/core";
import { apiClient } from "../ApiClient";
import MenuIcon from "@material-ui/icons/Menu";
import DashboardPlot from "./DashboardPlot";
import DashboardParamsSelector from "./DashboardParamsSelector";


interface DashboardState {
    allKeywords: string[];
    selectedKeywords: string[];
    from: moment.Moment;
    to: moment.Moment;
    mentions: [];
    sentiments: [];
}

export class Dashboard extends React.Component<{}, DashboardState> {
    constructor(props: {}) {
        super(props);
        this.state = {
            allKeywords: [],
            selectedKeywords: [],
            mentions: [],
            sentiments: [],
            from: moment().add(-7, "days").startOf("day"),
            to: moment().startOf("day")
        };

        setInterval(() => { this.downloadMentions(); this.downloadKeywords(); }, 5000);
    }

    componentDidMount() {
        this.downloadKeywords();
    }

    render() {
        return <div className="flex-grow-1">
            <AppBar position="fixed">
                <Toolbar>
                    <IconButton color="inherit">
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6" color="inherit">
                        Sentinel
                        </Typography>
                </Toolbar>
            </AppBar>

            <Grid container spacing={8}>
                <Grid container item xs={5} spacing={8} direction="column" alignItems="center">
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
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid item xs={5}>
                    </Grid>
                </Grid>

                <Grid container item xs={7} spacing={8} direction="column">
                    <Grid item>
                        <DashboardPlot title="Sentiment plot" plotData={this.state.sentiments} />
                    </Grid>
                    <Grid item>
                        <DashboardPlot title="Mentions count" plotData={this.state.mentions} />
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
        const mentionsPromise = apiClient.getMentionsCount(
            this.state.from,
            this.state.to,
            this.state.selectedKeywords
        );

        const sentimentsPromise = apiClient.getMentionsSentimentScores(
            this.state.from,
            this.state.to,
            this.state.selectedKeywords
        );

        const mentions = await mentionsPromise;
        const sentiments = await sentimentsPromise;

        this.setState({ sentiments, mentions });
    }
}
