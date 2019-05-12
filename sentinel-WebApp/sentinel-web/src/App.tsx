import * as React from "react";
import { Dashboard } from "./Components/Dashboard";
import Amplify from "@aws-amplify/core";
import Auth from "@aws-amplify/auth";
// import { withAuthenticator } from "aws-amplify-react";

Amplify.configure({
  Auth: {
    region: "eu-central-1",
    userPoolId: "eu-central-1_mADHJQzc7",
    userPoolWebClientId: "2r49jo9f4mf92aspdpemmp2u1v"
  }
});

// Amplify.configure(awsmobile);

Auth.signIn("dardzinskim@student.mini.pw.edu.pl", "DudaDuda1")
  .then(res => console.log(res))
  .catch(res => console.error(res));



const App: React.FC = () => {
  return <Dashboard/>;
};

export default App;

// export default withAuthenticator(App, true);
