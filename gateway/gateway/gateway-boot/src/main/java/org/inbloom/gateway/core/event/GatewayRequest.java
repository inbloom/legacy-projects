package org.inbloom.gateway.core.event;

/**
 * @author benjaminmorgan
 *         Date: 4/11/14
 */
public class GatewayRequest<X> {

    private final X payload;
    private final GatewayAction action;


    public GatewayRequest(GatewayAction action, X payload) {
        this.action = action;
        this.payload = payload;
    }

    public X getPayload() {
        return payload;
    }

    public GatewayAction getAction() {
        return action;
    }

}
