import React, { useEffect, useState } from 'react';
import { Widget, addResponseMessage, toggleWidget } from 'react-chat-widget';
import { sendMessage, startConversation } from '../services/messageHandler';
import { handleAction } from '../services/actionHandler';

import 'react-chat-widget/lib/styles.css';

export default function WidgetContainer() {
    const [conversationID, setConversationID] = useState(String)

    useEffect(() => {
        toggleWidget();
        startConversation()
            .then((response) => {
                if (!response.conversation_id) {
                    addResponseMessage("Failed to initialise.");
                    return;
                }
                setConversationID(response.conversation_id);
                response.messages.forEach((message) => addResponseMessage(message));
            })
            .catch((err) => {
                addResponseMessage("Failed to initialise.");
                console.error(err);
            })
    }, []);

    const handleNewUserMessage = (message: string) => {
        sendMessage(message, conversationID).then((response) => {
            response.messages.forEach((message) => addResponseMessage(message));
            if (response.action) {
                handleAction(conversationID, response.action, addResponseMessage);
            }
        });
    };

    return (
        <Widget
            handleNewUserMessage={handleNewUserMessage}
            title="Weather bot"
            subtitle="A small project by Mitch"
            titleAvatar="https://i.pinimg.com/originals/92/43/b1/9243b10aa7605af02c83104e67cbac2b.jpg"
            profileAvatar="https://i.pinimg.com/originals/92/43/b1/9243b10aa7605af02c83104e67cbac2b.jpg"
            showTimeStamp={false}
            emojis={true}
            resizable={true}
        />
    );
}
