import * as React from "react";
import Plot from "react-plotly.js";
import * as moment from "moment";
import { FormControl, Select, InputLabel, MenuItem, Checkbox, ListItemText, TextField, Button, AppBar, Toolbar, Typography, IconButton, Grid } from "@material-ui/core";
import { apiClient } from "../ApiClient";
import { Mention } from "../Models/Mention";
import MenuIcon from "@material-ui/icons/Menu";



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
    }

    componentDidMount() {
        this.downloadKeywords();
    }

    render() {
        return <>
            <Grid container spacing={24} justify="center" alignItems="center" direction="column">
                <Grid item xs={12}>
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
                </Grid>
                <Grid item xs={10}>
                    <Plot
                        style={{ width: "100%", height: "100%" }}
                        useResizeHandler={true}
                        data={this.state.sentiments}
                        layout={{ title: "Sentiment Plot", autosize: true }}
                    />
                </Grid>
                <Grid item xs={10}>
                    <Plot
                        style={{ width: "100%", height: "100%" }}
                        useResizeHandler={true}
                        data={this.state.mentions}
                        layout={{ title: "Mentions count", autosize: true }}
                    />
                </Grid>
            </Grid>
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
        </>;
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

interface DashboardParamsSelectorProps {
    allKeywords: string[];
    selectedKeywords: string[];
    from: moment.Moment;
    to: moment.Moment;

    onSelectedKeywordsChanged: (keywords: string[]) => void;
    onFromChanged: (from: moment.Moment) => void;
    onToChanged: (from: moment.Moment) => void;
}


class DashboardParamsSelector extends React.Component<DashboardParamsSelectorProps> {
    render() {
        return <>
            <FormControl style={{ minWidth: 120 }}>
                <InputLabel>Keywords</InputLabel>
                <Select
                    multiple
                    multiline
                    value={this.props.selectedKeywords}
                    renderValue={(_: any) => this.props.selectedKeywords.join(",")}
                    onChange={this.onKeywordsChange}>
                    {
                        this.props.allKeywords.map(k => (
                            <MenuItem key={k} value={k}>
                                <Checkbox checked={this.props.selectedKeywords.indexOf(k) > -1} />
                                <ListItemText primary={k} />
                            </MenuItem>
                        ))
                    }
                </Select>
            </FormControl>
            <TextField
                label="From"
                type="date"
                value={this.formatDate(this.props.from)}
                onChange={this.onFromChange}
                InputLabelProps={{
                    shrink: true,
                }}
            />

            <TextField
                label="To"
                type="date"
                value={this.formatDate(this.props.to)}
                onChange={this.onTochange}
                InputLabelProps={{
                    shrink: true,
                }}
            />
        </>;
    }

    private onKeywordsChange = (event: React.ChangeEvent<HTMLSelectElement>, _: React.ReactNode) => {
        this.props.onSelectedKeywordsChanged(event.target.value as any as string[]);
        // typings are messed up, thus this ugly casting
    };

    private onFromChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = event.target.value;
        this.props.onFromChanged(moment.utc(value));
    };

    private onTochange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = event.target.value;
        this.props.onToChanged(moment.utc(value));
    };

    private formatDate = (date: moment.Moment) => date.format("YYYY-MM-DD");
}
