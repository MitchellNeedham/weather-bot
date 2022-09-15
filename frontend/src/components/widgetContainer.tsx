import React, { useEffect, useState } from 'react';
import { Widget, addResponseMessage } from 'react-chat-widget';
import { sendMessage, startConversation } from '../services/messageHandler';
import { handleAction } from '../services/actionHandler';

import 'react-chat-widget/lib/styles.css';

export default function WidgetContainer() {
    const [conversationID, setConversationID] = useState(String)

    useEffect(() => {
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
        />
    );
}
