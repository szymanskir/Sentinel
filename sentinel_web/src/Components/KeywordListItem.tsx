import * as React from "react";
import { ListItem, ListItemText, ListItemSecondaryAction, IconButton, Button, TextField } from "@material-ui/core";
import DeleteIcon from "@material-ui/icons/Delete";
import EditIcon from "@material-ui/icons/Edit";
import CheckIcon from "@material-ui/icons/Check";

export interface KeywordListItemProps {
    name: string;
    isEditable: boolean;
    onStartEditCallback: Function;
    onEndEditCallback: Function;
    onDelete: Function;
}

export interface KeywordsListItemState {
    keywordItemName: string;
}

class KeywordListItem extends React.Component<KeywordListItemProps, KeywordsListItemState> {
    constructor(props: KeywordListItemProps) {
        super(props);
        this.state = {
            keywordItemName: this.props.name
        };
    }

    private saveKeywordItemName(event: any) {
        this.setState({
            keywordItemName: event.target.value.toString(),
        });
    }

    private createEditableItem() {
        return <ListItem alignItems="flex-start">
            <ListItemText>
                <TextField defaultValue={this.props.name} placeholder={"Enter keyword..."} onChange={(event) => this.saveKeywordItemName(event)} autoFocus />
            </ListItemText>
            <ListItemSecondaryAction>
                <Button onClick={() => this.props.onEndEditCallback(this.props.name, this.state.keywordItemName)}>
                    <CheckIcon />
                    Ok
                </Button>
            </ListItemSecondaryAction>
        </ListItem>;
    }

    private createDefaultItem(): React.ReactNode {
        return <ListItem alignItems="flex-start">
            <ListItemText primary={this.props.name} />
            <ListItemSecondaryAction>
                <Button aria-label="Edit" onClick={() => this.props.onStartEditCallback()}>
                    <EditIcon />
                    Edit
            </Button>
                <Button aria-label="Delete" onClick={() => this.props.onDelete()}>
                    <DeleteIcon />
                    Delete
                </Button>
            </ListItemSecondaryAction>
        </ListItem>;
    }


    render() {
        return <>
            {this.props.isEditable ? this.createEditableItem() : this.createDefaultItem()}
        </>;
    }
}

export default KeywordListItem;
