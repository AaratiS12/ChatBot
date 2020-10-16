import * as React from 'react';
import {Li} from "./Li";


export function Chatbot (props) {
    return (
        <div>
        <ul>
      {props.displayTexts.map((x) => (<Li value = {x}/>))}
      </ul>
        </div>
        )
}