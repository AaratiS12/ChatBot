import * as React from 'react';
import Linkify from 'react-linkify';

export function Li (props) {
   
    let m = props.msg
    let indexOf = m.indexOf(":");
    let username = m.substring(0,indexOf);
    let messageWOname = m.substring(indexOf+2, m.length);
    let lastFour = messageWOname.substr(messageWOname.length - 4);
    let Isimage = null
     if (lastFour == ".png" || lastFour==".gif" || lastFour==".jpg"){
        Isimage = true
     }
    else{
        Isimage = false
    }
    
    if (Isimage) {
        if(props.user !== username){
        return <Linkify><li id="left_list_element">{username}: <img src={messageWOname} width="40" height="40"/></li></Linkify>;
    }
        return <Linkify><li id="right_list_element">{username}: <img src={messageWOname} width="40" height="40"/></li></Linkify>;
     
    }
    else {
        if(props.user !== username){
        return <Linkify><li  id="left_list_element">{props.msg}</li></Linkify>;
        }
        return <Linkify><li id="right_list_element" >{props.msg}</li> </Linkify>;
    }
    
}
