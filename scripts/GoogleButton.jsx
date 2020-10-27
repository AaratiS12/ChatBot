import * as React from 'react';
import ReactDOM from 'react-dom';
import GoogleLogin from 'react-google-login';
import { Socket } from './Socket';
/* eslint no-console: ["error", { allow: ["log"] }] */
function handleSubmit(response) {
  console.log(response);
  const name = response.profileObj.email;
  Socket.emit('new google user', {
    name,
  });

  console.log(`Sent the name ${name} to server!`);
}

export function GoogleButton() {
  return (
    <GoogleLogin
      clientId="996903865463-g40t530m1jb7bvqq2evel1dcjej6td8d.apps.googleusercontent.com"
      buttonText="Login"
      onSuccess={handleSubmit}
      onFailure={handleSubmit}
      cookiePolicy="single_host_origin"
    />
  );
}
export default GoogleButton;
