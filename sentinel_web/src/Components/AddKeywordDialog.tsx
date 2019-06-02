import * as React from "react";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import { TextField, Button } from "@material-ui/core";

export interface AddKeywordDialogProps {
    isOpen: boolean;
    onCancel: () => void;
    onSubmit: (keywordName: string) => void;
}

export interface AddKeywordDialogState {
    keywordName: string;
}

class AddKeywordDialog extends React.Component<AddKeywordDialogProps, AddKeywordDialogState> {
    render() {
        return (
            <Dialog open={this.props.isOpen}>
                <DialogTitle>Add new keyword</DialogTitle>
                <DialogContent>
                    <DialogContentText>Specify the keyword that you would like to track.</DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="Keyword name"
                        fullWidth
                        onChange={(event) => this.setState({ keywordName: event.target.value })}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => this.props.onCancel()} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={() => this.props.onSubmit(this.state.keywordName)} color="primary">
                        Add
                    </Button>
                </DialogActions>
            </Dialog>
        );
    }
}

export default AddKeywordDialog;
