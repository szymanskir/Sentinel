import * as React from "react";
import { Drawer, List, ListItem, ListItemIcon, ListItemText } from "@material-ui/core";
import HomeIcon from "@material-ui/icons/Home";
import AnnouncementIcon from "@material-ui/icons/Announcement";

export interface DashboardDrawerProps {
    isOpen: boolean;
    onDrawerClose: () => void;
}

export interface DashboardDrawerState {
}

class DashboardDrawer extends React.Component<DashboardDrawerProps, DashboardDrawerState> {
    render() {
        return <Drawer anchor="left" open={this.props.isOpen} onClose={this.props.onDrawerClose}>
            <List>
                <ListItem button key="Home">
                    <ListItemIcon><HomeIcon/></ListItemIcon>
                    <ListItemText primary={"Home"}/>
                </ListItem>
                <ListItem button key="Keywords">
                    <ListItemIcon><AnnouncementIcon/></ListItemIcon>
                    <ListItemText primary={"Keywords"}/>
                </ListItem>
            </List>
        </Drawer>;
    }
}

export default DashboardDrawer;
