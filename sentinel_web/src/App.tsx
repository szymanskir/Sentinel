import * as React from "react";
import { Dashboard } from "./Components/Dashboard";
import Amplify from "@aws-amplify/core";
import { withAuthenticator } from "aws-amplify-react";
import config from "config";

Amplify.configure({
  Auth: {
    region: config.awsRegion,
    userPoolId: config.cognitoUserPoolId,
    userPoolWebClientId: config.cognitoWebClientId
  }
});

const App: React.FC = () => {
  return <Dashboard />;
};

export default withAuthenticator(App, true);
