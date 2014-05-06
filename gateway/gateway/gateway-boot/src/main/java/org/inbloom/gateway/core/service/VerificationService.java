package org.inbloom.gateway.core.service;

import org.inbloom.gateway.common.domain.AccountValidation;
import org.inbloom.gateway.common.domain.Verification;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.springframework.stereotype.Service;


/**
 * Created with IntelliJ IDEA.
 * User: benjaminmorgan
 * Date: 3/25/14
 * Time: 8:46 AM
 * To change this template use File | Settings | File Templates.
 */
@Service
public interface VerificationService {

    static final int VERIFICATION_TIMEOUT = 3*24*60*60*1000; //3 days

    GatewayResponse<Verification> createVerification(GatewayRequest<Verification> createEvent);
    GatewayResponse<Verification> validateAccountSetup(GatewayRequest<AccountValidation> validateEvent);
    GatewayResponse<Verification> modifyVerification(GatewayRequest<Verification> modifyEvent);
    GatewayResponse<Verification> retrieveVerification(GatewayRequest<Verification> retrieveEvent);

}
