package org.inbloom.gateway.core.event;

import org.inbloom.gateway.common.status.GatewayStatus;
import org.inbloom.gateway.common.status.Status;

/**
 * @author benjaminmorgan
 *         Date: 4/11/14
 */
public class GatewayResponse<X> {

    private X payload;
    private GatewayAction action;
    private GatewayStatus statusContainer;

    public GatewayResponse(GatewayAction action, X payload, GatewayStatus statusContainer) {
        this.action = action;
        this.payload = payload;
        this.statusContainer = statusContainer;
    }

    public GatewayResponse(GatewayAction action, X payload, Status status) {
        this.action = action;
        this.payload = payload;
        this.statusContainer = new GatewayStatus(status);
    }

    public GatewayResponse(GatewayAction action, X payload, Status status, String statusMessage) {
        this.action = action;
        this.payload = payload;
        this.statusContainer = new GatewayStatus(status, statusMessage);
    }

    public GatewayAction getAction() {
        return action;
    }

    public X getPayload() {
        return payload;
    }

    public GatewayStatus getStatusContainer() {
        return statusContainer;
    }

    public Status getStatus(){
        if(statusContainer != null) {
            return statusContainer.getStatus();
        }
        else{
            return null;
        }
    }

}
