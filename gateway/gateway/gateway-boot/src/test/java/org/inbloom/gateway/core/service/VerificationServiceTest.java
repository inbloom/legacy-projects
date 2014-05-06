package org.inbloom.gateway.core.service;


import org.inbloom.gateway.common.domain.AccountValidation;
import org.inbloom.gateway.common.domain.Credentials;
import org.inbloom.gateway.common.domain.Verification;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.credentials.CredentialService;
import org.inbloom.gateway.persistence.service.VerificationPersistenceService;
import org.inbloom.gateway.util.keyService.KeyGenerator;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.mockito.runners.MockitoJUnitRunner;
import org.springframework.core.env.Environment;

import java.util.Date;

import static org.inbloom.gateway.fixture.VerificationFixture.*;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.mockito.Matchers.any;

/**
 * Created By: paullawler
 */
@RunWith(MockitoJUnitRunner.class)
public class VerificationServiceTest {

    @Mock
    private VerificationPersistenceService persistence;

    @Mock
    private CredentialService credentialer;

    @Mock
    private Environment env;

    @Mock
    private KeyGenerator keyGenerator;

    @InjectMocks
    private VerificationServiceHandler verificationService;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void shouldFailIfVerificationHasExpired() {
        GatewayRequest<AccountValidation> validate = new GatewayRequest<AccountValidation>(GatewayAction.RETRIEVE, accountValidation());

        Mockito.when(persistence.retrieveForAccountValidation(validate))
                .thenReturn(expiredVerificationEvent(validate.getPayload().getValidationDate()));

        GatewayResponse<Verification> validated = verificationService.validateAccountSetup(validate);
        assertEquals(Status.EXPIRED, validated.getStatus());
    }

    @Test
    public void shouldValidateAnAppProviderAccount() {
        GatewayRequest<AccountValidation> validate = new GatewayRequest<AccountValidation>(GatewayAction.RETRIEVE, accountValidation());

        Mockito.when(persistence.retrieveForAccountValidation(validate))
                .thenReturn(validVerificationEvent(validate.getPayload().getValidationDate()));

        Mockito.when(credentialer.createCredentials(any(GatewayRequest.class)))
                .thenReturn(new GatewayResponse<Credentials>(GatewayAction.CREATE,
                        new Credentials("Santino", "Corleone", "sonny.corleone@mailinator.com", "s@ntin0rul3z") , Status.SUCCESS));

        Mockito.when(persistence.modifyVerification(any(GatewayRequest.class)))
                .thenReturn(modifiedVerificationEvent(validate.getPayload().getValidationDate()));


        GatewayResponse<Verification> validated = verificationService.validateAccountSetup(validate);
        assertEquals(Status.SUCCESS, validated.getStatus());
        assertTrue(validated.getPayload().isVerified());
    }

    // FIXTURES

    private GatewayResponse<Verification> expiredVerificationEvent(Date validationDate) {
        return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, expiredVerification(validationDate), Status.SUCCESS);
    }

    private GatewayResponse<Verification> validVerificationEvent(Date validationDate) {
        return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, validVerification(validationDate), Status.SUCCESS);
    }

    private GatewayResponse<Verification> modifiedVerificationEvent(Date validationDate) {
        Verification v = validVerification(validationDate);
        v.validate();
        return new GatewayResponse<Verification>(GatewayAction.MODIFY, v, Status.SUCCESS);
    }

}
