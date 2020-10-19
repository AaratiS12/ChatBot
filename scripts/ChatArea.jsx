import React, { useEffect, useState } from "react";
import {Li} from "./Li";
import { Socket } from './Socket';

export function ChatArea (props) {
    
    const [texts, updateTexts] = useState( () => {return [];} );
    const [user_name, update_Username] = useState( () => {return "";} );
    
   
    function addText(text){
        updateTexts((oldList) => oldList.concat(text));
    }
   
   function newData() {
         React.useEffect(() => {
            Socket.on('chatArea', (data) => {
                console.log("Received google username from server: " + data['uname']);
                update_Username(data['uname']);
            })
        }, []);  
    
    
        React.useEffect(() => {
            Socket.on('text received', (data) => {
                console.log("Received text from server: " + data['text']);
                addText(data['text']);
            })
        }, []); 
    }
    newData();
    return (
        <div id="chatarea">
      <ol>
      {
        texts.map((message,index)=><Li key={index}  msg={message} user={user_name}/>)
      }
      </ol>
        </div>
       
        )
}