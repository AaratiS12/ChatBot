import React, { useState } from 'react';
import { Socket } from './Socket';


export function Input (props) {
    
     const [textBoxValue, updatetextBoxValue] = useState( 
        () => {return "";}
        );
    
 function handleSubmit(event) {
    updatetextBoxValue("");
    event.preventDefault();
    Socket.emit('new message', {
        'new message': textBoxValue,
    });
   
  }
    return (
         <div id ="inputArea">
    <form onSubmit={handleSubmit}>
        <label>
          <input type="text" size="133" value={textBoxValue} onChange={e => updatetextBoxValue(e.target.value)} />
        </label>
        <input type="submit" value="Submit" />
      </form>
    </div> 
    );
   
}
