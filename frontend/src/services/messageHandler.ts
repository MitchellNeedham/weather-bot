import axios from "axios";
import { MessageResponseAction } from './actionHandler';

export interface MessageResponse {
    conversation_id?: string;
    messages: string[];
    action?: MessageResponseAction;
}

export async function sendMessage(message: string, conversationID: string): Promise<MessageResponse> {
    const payload = {
        conversation_id: conversationID,
        message
    }
    try {
        const res = await axios.post("/api/conversation/message-handler", payload);
        return res.data;
    } catch (err) {
        console.error(err);
        return {messages: ["Something went wrong."]}
    }
}

export async function startConversation(): Promise<MessageResponse> {
    try {
        const res = await axios.get("/api/conversation/start-conversation");
        return res.data;
    } catch (err) {
        console.error(err);
        return {messages: ["Something went wrong."]}
    }
}