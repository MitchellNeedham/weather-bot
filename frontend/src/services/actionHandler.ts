import { getGeolocation } from "./geolocation";
import { MessageResponse } from "./messageHandler";

export enum MessageResponseAction {
    GEO_LOC = "GEO_LOC",
};

export function handleAction(
        conversationID: string,
        action: MessageResponseAction,
        addMessageCallback: (text: string) => void): Promise<MessageResponse> | undefined {
    switch (action) {
        case MessageResponseAction.GEO_LOC:
            getGeolocation(conversationID, addMessageCallback)
            break;
        default:
            return;
    }

}