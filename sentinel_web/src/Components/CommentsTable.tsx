import * as React from "react";
import MUIDataTable, { MUIDataTableOptions } from "mui-datatables";

export interface CommentsTableProps {
    mentions: any;
}

export interface CommentsTableState {

}

class CommentsTable extends React.Component<CommentsTableProps, CommentsTableState> {
    render() {
        const columns = ["author", "sentimentScore", "keyword", "date"];
        const options = {
            filterType: "multiselect",
            responsive: "scroll",
            selectableRows: false
        } as MUIDataTableOptions;

        return <MUIDataTable
            title={"Mentions data"}
            data={this.props.mentions}
            columns={columns}
            options={options}/>;
    }
}

export default CommentsTable;
