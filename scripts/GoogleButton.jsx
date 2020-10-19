import * as React from 'react';
import { Socket } from './Socket';
import ReactDOM from 'react-dom';
import GoogleLogin from 'react-google-login';


function handleSubmit(response) {
    console.log(response["profileObj"]["email"])
    let name = response["profileObj"]["email"]
    Socket.emit('new google user', {
        'name': name,
    });
    
    console.log('Sent the name ' + name + ' to server!');
}

export function GoogleButton() {
    return (
            <GoogleLogin
    clientId="996903865463-g40t530m1jb7bvqq2evel1dcjej6td8d.apps.googleusercontent.com"
    buttonText="Login"
    onSuccess={handleSubmit}
    onFailure={handleSubmit}
    cookiePolicy={'single_host_origin'}
  />
    );
}