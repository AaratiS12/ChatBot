import React, { useEffect, useState } from "react";
import {Li} from "./Li";
import { Socket } from './Socket';

export function ChatArea (props) {
    
    const [texts, updateTexts] = useState( () => {return [];} );
    const [user_name, update_Username] = useState( () => {return "";} );
    
   
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
            Socket.on('text received', (data) => {
                console.log("Received text from server: " + data['text']);
                addText(data['text']);
            })
        }, []); 
        
    }
    newNumber();
    return (
       
        <div id="chatarea">
      <ol>
      {
        texts.map((message,index)=><Li id="list_element" key={index}  msg={message} />)
      }
      </ol>
        </div>
       
        )
}