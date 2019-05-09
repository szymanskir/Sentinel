import React from 'react';
import Plot from 'react-plotly.js';
import moment from 'moment';
import { FormControl, Select, InputLabel, MenuItem, Checkbox, ListItemText, TextField } from '@material-ui/core';

const keywords = ['life', 'nike', 'javascript'];


interface DashboardState {
    selectedKeywords: String[];
    from: moment.Moment;
    to: moment.Moment;
}



export class Dashboard extends React.Component<{}, DashboardState> {
    constructor(props: {}) {
        super(props);
        this.state = {
            selectedKeywords: [],
            from: moment().add(-7, 'days').startOf('day'),
            to: moment().startOf('day')
        };
    }

    render() {
        return <>
            <DashboardParamsSelector
                selectedKeywords={this.state.selectedKeywords}
                from={this.state.from}
                to={this.state.to}
                onSelectedKeywordsChanged={selectedKeywords => this.setState({ selectedKeywords })}
                onFromChanged={from => this.setState({ from })}
                onToChanged={to => this.setState({ to })}
            />

            <br />

            <Plot
                data={
                    [
                        {
                            x: [1, 2, 3],
                            y: [2, 6, 3],
                            type: 'scatter',
                            mode: 'lines+markers',
                            marker: { color: 'red' },
                        },
                        {
                            type: 'bar',
                            x: [1, 2, 3], y: [2, 5, 3]
                        },
                    ]}
                layout={{ title: 'A Fancy Plot' }
                }
            />
        </>;
    }
}


interface DashboardParamsSelectorProps {
    selectedKeywords: String[];
    from: moment.Moment;
    to: moment.Moment;

    onSelectedKeywordsChanged: (keywords: String[]) => void;
    onFromChanged: (from: moment.Moment) => void;
    onToChanged: (from: moment.Moment) => void;
};


class DashboardParamsSelector extends React.Component<DashboardParamsSelectorProps> {
    render() {
        return <>
            <FormControl style={{ minWidth: 120 }}>
                <InputLabel>Keywords</InputLabel>
                <Select
                    multiple
                    multiline
                    value={this.props.selectedKeywords}
                    renderValue={(_: any) => this.props.selectedKeywords.join(',')}
                    onChange={this.onKeywordsChange}>
                    {
                        keywords.map(k => (
                            <MenuItem key={k} value={k}>
                                <Checkbox checked={this.props.selectedKeywords.indexOf(k) > -1} />
                                <ListItemText primary={k} />
                            </MenuItem>
                        ))
                    }
                </Select>
            </FormControl>
            <TextField
                label='From'
                type='date'
                value={this.formatDate(this.props.from)}
                onChange={this.onFromChange}
                InputLabelProps={{
                    shrink: true,
                }}
            />

            <TextField
                label='To'
                type='date'
                value={this.formatDate(this.props.to)}
                onChange={this.onTochange}
                InputLabelProps={{
                    shrink: true,
                }}
            />
        </>;
    }

    private onKeywordsChange = (event: React.ChangeEvent<HTMLSelectElement>, _: React.ReactNode) => {
        this.props.onSelectedKeywordsChanged(event.target.value as any as String[]);
        // typings are messed up, thus this ugly casting
    };

    private onFromChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = event.target.value;
        this.props.onFromChanged(moment(value));
    };

    private onTochange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = event.target.value;
        this.props.onToChanged(moment(value));
    };

    private formatDate = (date: moment.Moment) => date.format('YYYY-MM-DD');
}
