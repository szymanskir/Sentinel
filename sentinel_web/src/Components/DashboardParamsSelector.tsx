import * as React from "react";
import * as moment from "moment";
import { FormControl, InputLabel, Select, MenuItem, Checkbox, ListItemText, TextField } from "@material-ui/core";


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
                onChange={this.onToChange}
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

    private onToChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = event.target.value;
        this.props.onToChanged(moment.utc(value));
    };

    private formatDate = (date: moment.Moment) => date.format("YYYY-MM-DD");
}

export default DashboardParamsSelector;
