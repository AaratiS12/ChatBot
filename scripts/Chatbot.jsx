import * as React from 'react';
import {Li} from "./Li";

 /* eslint no-console: ["error", { allow: ["log"] }] */
export function Chatbot (props) {
    return (
        <div>
        <ul>
      {props.displayTexts.map((x) => (<Li value = {x}/>))}
      </ul>
        </div>
        )
}