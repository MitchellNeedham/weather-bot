import axios from "axios";
import { MessageResponse } from "./messageHandler";

export interface GeoLocation {
    longitude: number;
    latitude: number;
}

export function getGeolocation(conversationID: string, addMessageCallback: (text: string) => void): GeoLocation | undefined {
    if (!navigator.geolocation) {
        return;
    }
    navigator.geolocation.getCurrentPosition(
        (position) => postLocation(conversationID, position, addMessageCallback),
        () => postLocation(conversationID, null, addMessageCallback)
    )
}

function postLocation(conversationID: string, position: any, addMessageCallback: (text: string) => void): void {
    const payload = {
        conversation_id: conversationID,
        latitude: position?.coords?.latitude,
        longitude: position?.coords?.longitude,
        failed: !(position?.coords?.latitude && position?.coords?.longitude)
    }
    if (!payload.failed) {
        addMessageCallback("Thank you! Give me a moment to check for you.")
    }
    axios.post('/api/conversation/set-location', payload)
        .then(({ data }) => {
            data.messages.forEach((message: string) => addMessageCallback(message));
        })
        .catch((err) => {
            console.error(err)
            addMessageCallback("Something went wrong.")
        });
}

