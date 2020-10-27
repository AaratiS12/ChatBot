import React, { useEffect, useState } from 'react';
import { Li } from './Li';
import { Socket } from './Socket';

export function ChatArea() {
  const [texts, updateTexts] = useState(() => []);
  const [userName, updateUsername] = useState(() => '');

  function addText(text) {
    updateTexts((oldList) => oldList.concat(text));
  }

  function newData() {
    React.useEffect(() => {
      Socket.on('chatArea', (data) => {
        /* eslint no-console: ["error", { allow: ["log"] }] */
        console.log(`Received google username from server: ${data.uname}`);
        updateUsername(data.uname);
      });
    }, []);

    React.useEffect(() => {
      Socket.on('text received', (data) => {
        /* eslint no-console: ["error", { allow: ["log"] }] */
        console.log(`Received text from server: ${data.text}`);
        addText(data.text);
      });
    }, []);
  }
  newData();
  return (
    <div id="chatarea">
      <ol>
        {
        texts.map((message, index) => <Li key={index} msg={message} user={userName} />)
      }
      </ol>
    </div>

  );
}

export default ChatArea;
