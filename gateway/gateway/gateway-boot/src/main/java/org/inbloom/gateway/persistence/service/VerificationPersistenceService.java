package org.inbloom.gateway.persistence.service;


import org.inbloom.gateway.common.domain.AccountValidation;
import org.inbloom.gateway.common.domain.Verification;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;

/**
 * Created by lloydengebretsen on 3/21/14.
 */
public interface VerificationPersistenceService {

    public GatewayResponse<Verification> createVerification(GatewayRequest<Verification> createVerificationEvent);
    public GatewayResponse<Verification> retrieveForAccountValidation(GatewayRequest<AccountValidation> validateAccountSetupEvent);
    public GatewayResponse<Verification> retrieveVerification(GatewayRequest<Verification> retrieveVerificationEvent);
    public GatewayResponse<Verification> modifyVerification(GatewayRequest<Verification> modifyVerificationEvent);
}
