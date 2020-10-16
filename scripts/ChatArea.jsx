import React, { useEffect, useState } from "react";
import {Li} from "./Li";
import { Socket } from './Socket';


export function ChatArea (props) {
    
    const [texts, updateTexts] = useState( () => {return [];} );
    const [user_name, update_Username] = useState( () => {return "uname";} );
    
    const [messages, updateMessages] = React.useState([]);
    const [count, updateCount] = React.useState(0);
   
    function addText(text){
        updateTexts((oldList) => oldList.concat(text));
    }
   
   function newNumber() {
         React.useEffect(() => {
            Socket.on('user name', (data) => {
                console.log("Received username from server: " + data['username']);
                update_Username(data['username']);
            })
        }, []);  
    
         React.useEffect(() => {
            Socket.on('messages received', (data) => {
                console.log("Received message from server: " + data['allMessages']);
                updateMessages(data['allMessages']);
            })
        }, []); 
        
        React.useEffect(() => {
            Socket.on('text received', (data) => {
                console.log("Received text from server: " + data['text']);
                addText(data['text']);
            })
        }, []); 
        
        React.useEffect(() => {
            Socket.on('connection', (data) => {
                console.log("Received connection status from server: " + data['connection']);
                updateCount(data['connection']);
            })
        }, []); 
    }
    newNumber();
    return (
       
        <div id="chatarea">
      <ol>
      {
          texts.map(
            (message,index)=><li id="list_element" key={index}>{message}</li>    )
      }
      </ol>
        </div>
       
        )
}