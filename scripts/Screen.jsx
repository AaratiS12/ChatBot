import React from 'react';
import {Input}  from './Input';
import {ChatArea}  from './ChatArea';
import { Socket } from './Socket';

export function Screen () {
    
    const [count, updateCount] = React.useState(0);
    function newNumber() {
        React.useEffect(() => {
            Socket.on('connection', (data) => {
                console.log("Received another connection status from server: " + data['connection']);
                updateCount(data['connection']);
            })
        }, []); 
    }
    newNumber();
    return <div id="screenarea">
     <p id= "count_header">Num of users: {count}</p>
    <ChatArea />
    <Input />
    </div>;
}