package org.inbloom.gateway.fixture;

import org.inbloom.gateway.Gateway;
import org.inbloom.gateway.common.domain.Verification;
import org.inbloom.gateway.common.status.GatewayStatus;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;

/**
 * @author benjaminmorgan
 *         Date: 3/27/14
 */
public class VerificationEventFixtures {

    /**create**/
    public static GatewayRequest<Verification> buildCreateVerificationEvent() {
        Verification payload = new Verification();
        payload.setUser(UserFixture.buildUser());
        return new GatewayRequest<Verification>(GatewayAction.CREATE, payload);
    }

    /**retrieve**/
    public static GatewayRequest<Verification> buildRetrieveVerificationEvent(String token) {
        Verification payload = new Verification();
        payload.setToken(token);
        return new GatewayRequest<Verification>(GatewayAction.RETRIEVE, payload);
    }

    /**created**/
    public static GatewayResponse<Verification> buildSuccessCreatedVerificationEvent(Long userId, Long verificationId) {
        return new GatewayResponse<Verification>(GatewayAction.CREATE, VerificationFixture.buildUnverifiedVerification(1l, 1l), Status.SUCCESS);
    }

    public static GatewayResponse<Verification> buildNotFoundCreatedVerificationEvent() {
        return new GatewayResponse<Verification>(GatewayAction.CREATE, null, Status.NOT_FOUND);
    }

    /**modify**/
    public static GatewayRequest<Verification> buildModifyVerificationEvent() {
        return null; //TODO:
    }

    /**modified**/
    //TODO:

    /**retrieved**/
    public static GatewayResponse<Verification> buildSuccessRetrievedVerificationEvent(Verification verification) {
        return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, verification, Status.SUCCESS);
    }

    public static GatewayResponse<Verification> buildNotFoundRetrievedVerificationEvent() {
        return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, null, Status.NOT_FOUND);
    }

}
