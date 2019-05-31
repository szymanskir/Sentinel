import * as React from "react";
import { AppBar, Toolbar, Typography, IconButton, Drawer, List, ListItem, ListItemIcon, ListItemText } from "@material-ui/core";
import MenuIcon from "@material-ui/icons/Menu";
import HomeIcon from "@material-ui/icons/Home";
import AnnouncementIcon from "@material-ui/icons/Announcement";
import PowerSettingNew from "@material-ui/icons/PowerSettingsNew";

import { BrowserRouter as Router, Route, Link, RouteComponentProps } from "react-router-dom";
import { OverviewTabItem } from "./OverviewTabItem";
import KeywordsTabItem from "./KeywordsTabItem";
import { Auth } from "aws-amplify";


interface DashboardState {
    isDrawerOpen: boolean;
}

export class Dashboard extends React.Component<{}, DashboardState> {
    constructor(props: {}) {
        super(props);
        this.state = {
            isDrawerOpen: false,
        };
    }

    render() {
        return <div>
            <Router>
                <AppBar position="fixed">
                    <Toolbar>
                        <IconButton color="inherit" onClick={() => this.toggleDrawer(true)}>
                            <MenuIcon />
                        </IconButton>
                        <Typography variant="h6" color="inherit">
                            Sentinel
                        </Typography>
                    </Toolbar>
                </AppBar>
                <Drawer anchor="left" open={this.state.isDrawerOpen} onClose={() => this.toggleDrawer(false)}>
                    <List>
                        <ListItem button key="Home">
                            <ListItemIcon><HomeIcon /></ListItemIcon>
                            <ListItemText><Link to="/">Home</Link></ListItemText>
                        </ListItem>
                        <ListItem button key="Keywords">
                            <ListItemIcon><AnnouncementIcon /></ListItemIcon>
                            <ListItemText><Link to="/keywords">Keywords</Link></ListItemText>
                        </ListItem>
                        <ListItem button key="Logout">
                            <ListItemIcon><PowerSettingNew /></ListItemIcon>
                            <ListItemText><Link to="/logout">Logout</Link></ListItemText>
                        </ListItem>
                    </List>
                </Drawer>
                <div>
                    <Route exact path="/" component={OverviewTabItem} />
                    <Route path="/keywords" component={KeywordsTabItem} />
                    <Route exact path="/logout" render={this.logOut} />
                </div>
            </Router>
        </div>;
    }

    private logOut = (props: RouteComponentProps) => {
        Auth.signOut();
        return <Link to="/" />;
    }

    private toggleDrawer = async (shouldDrawerBeOpened: boolean) => {
        this.setState({ isDrawerOpen: shouldDrawerBeOpened });
    }
}
