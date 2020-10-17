import React from 'react';
import {Input}  from './Input';
import {ChatArea}  from './ChatArea';
import { Socket } from './Socket';
import {GoogleButton} from './GoogleButton'

export function Screen () {
    
    const [count, updateCount] = React.useState(0);
    const [isLoggedIn, updateLogin] = React.useState(true);
    function newNumber() {
        React.useEffect(() => {
            Socket.on('connection', (data) => {
                console.log("Received a connection from server: " + data['connection']);
                updateCount(data['connection']);
            })
        }, []); 
        
        React.useEffect(() => {
            Socket.on('google user', (data) => {
                console.log("Received google login from server: " + data['connection']);
                updateLogin(true);
            })
        }, []); 
    }
    newNumber();
    if (isLoggedIn) {
    return <div>
     <p id= "count_header">Number of users: {count}</p>
    <ChatArea />
    <Input />
    </div>;}
    
     return <div id="screenarea">
     <h1>Please Login</h1>
     <GoogleButton />
    </div>;
}