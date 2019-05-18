import * as React from "react";
import Plot from "react-plotly.js";
import { Card, CardHeader, Typography, CardContent, Grid } from "@material-ui/core";

export interface DashboardPlotProps {
    plotData: any;
    title: string;
}

class DashboardPlot extends React.Component<DashboardPlotProps, {}> {
    render() {
        return <>
            <Card>
                <CardContent>
                    <Typography variant="h5" component="h6">
                        {this.props.title}
                    </Typography>
                    <Plot style={{ width: "100%", height: "100%" }}
                        useResizeHandler={true}
                        data={this.props.plotData}
                        layout={{ autosize: true, margin: {t: 30, b: 30, l: 50, r: 10 } }} />
                </CardContent>
            </Card>
        </>;
    }
}

export default DashboardPlot;
