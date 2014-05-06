package org.inbloom.gateway.persistence.service;


import org.inbloom.gateway.Gateway;
import org.inbloom.gateway.common.domain.AccountValidation;
import org.inbloom.gateway.common.domain.ApplicationProvider;
import org.inbloom.gateway.common.domain.Verification;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.core.service.VerificationService;
import org.inbloom.gateway.fixture.ApplicationProviderFixture;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.transaction.TransactionConfiguration;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.transaction.annotation.Transactional;

import static org.junit.Assert.*;

/**
 * Created By: paullawler
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(classes = Gateway.class)
@WebAppConfiguration
@Transactional
@TransactionConfiguration(defaultRollback = true)
public class VerificationPersistenceTest {

    @Autowired
    private ApplicationProviderPersistenceService providerService;

    @Autowired
    private VerificationPersistenceService verificationService;

    private GatewayResponse<Verification> created;

    @Before
    public void setUp() {
        GatewayRequest<ApplicationProvider> register = new GatewayRequest<ApplicationProvider>(GatewayAction.CREATE, ApplicationProviderFixture.buildAppProvider1(null));
        GatewayResponse<ApplicationProvider> registered = providerService.createApplicationProvider(register);
        Verification payload = new Verification();
        payload.setUser(registered.getPayload().getUser());
        created = verificationService.createVerification(new GatewayRequest<Verification>(GatewayAction.CREATE, payload));
    }

    @Test
    public void shouldRetrieveAVerificationForAccountValidation() {
        AccountValidation accountValidation = new AccountValidation(created.getPayload().getToken(), "passwerd");
        GatewayResponse<Verification> retrieved = verificationService.retrieveForAccountValidation(
                new GatewayRequest<AccountValidation>(GatewayAction.RETRIEVE, accountValidation));
        assertNotNull(retrieved.getPayload().getUser());
    }

    @Test
    public void shouldReturnNotFoundIfInvalidToken() {
        Verification payload = new Verification();
        payload.setToken("i-am-an-invalid-token");
        GatewayResponse<Verification> retrieved = verificationService.retrieveVerification(new GatewayRequest<Verification>(GatewayAction.RETRIEVE, payload));
        assertEquals(Status.NOT_FOUND, retrieved.getStatus());
    }

    @Test
    public void shouldModifyAVerification() {
        Verification verification = created.getPayload();
        verification.activate(VerificationService.VERIFICATION_TIMEOUT);
        GatewayResponse<Verification> modified = verificationService.modifyVerification(new GatewayRequest<Verification>(GatewayAction.MODIFY, verification));
        assertEquals(Status.SUCCESS, modified.getStatus());
    }

}
