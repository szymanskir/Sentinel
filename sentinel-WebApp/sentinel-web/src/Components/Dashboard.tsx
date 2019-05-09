import React from 'react';
import Plot from 'react-plotly.js';
import { FormControl, Select, InputLabel, MenuItem, Checkbox, ListItemText } from '@material-ui/core';

const keywords = ['life', 'nike', 'javascript'];


interface DashboardState {
    selectedKeywords: String[];
}



export class Dashboard extends React.Component<{}, DashboardState> {
    constructor(props: {}) {
        super(props);
        this.state = {
            selectedKeywords: []
        };
    }

    render() {
        return <>
            <DashboardParamsSelector
                selectedKeywords={this.state.selectedKeywords}
                onSelectedKeywordsChanged={this.onSelectedKeywordsChanged}
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

    private onSelectedKeywordsChanged = (keywords: String[]) => {
        this.setState({ selectedKeywords: keywords });
    };
}


interface DashboardParamsSelectorProps {
    selectedKeywords: String[];

    onSelectedKeywordsChanged: (keywords: String[]) => void;
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
        </>;
    }

    private onKeywordsChange = (event: React.ChangeEvent<HTMLSelectElement>, _: React.ReactNode) => {
        this.props.onSelectedKeywordsChanged(event.target.value as any as String[]);
        // typings are messed up, this this ugly casting
    };
}
