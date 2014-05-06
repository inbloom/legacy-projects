package org.inbloom.gateway.core.service;

/**
 * Created By: paullawler
 */

import org.inbloom.gateway.Gateway;
import org.inbloom.gateway.common.domain.Verification;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.credentials.CredentialService;
import org.inbloom.gateway.fixture.VerificationEventFixtures;
import org.inbloom.gateway.persistence.service.VerificationPersistenceService;
import org.inbloom.gateway.util.keyService.KeyGenerator;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.jvnet.mock_javamail.Mailbox;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.core.env.Environment;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.transaction.TransactionConfiguration;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.transaction.annotation.Transactional;

import javax.mail.Message;
import javax.mail.internet.AddressException;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.mockito.Matchers.any;
import static org.mockito.Mockito.when;

/**
 * @author benjaminmorgan
 *         Date: 3/27/14
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(classes = Gateway.class)
@WebAppConfiguration
@Transactional
@TransactionConfiguration(defaultRollback = true)
public class VerificationServiceIntegrationTest {

    @Mock
    KeyGenerator keyGenerator;

    @Mock
    VerificationPersistenceService persistenceService;

    @Mock
    CredentialService credentialService;

    @Mock
    Environment env;

    @InjectMocks
    VerificationServiceHandler verificationService;

    @Before
    public void setup() {
        MockitoAnnotations.initMocks(this);
}

    @Test
    public void testCreateVerification() throws AddressException {

        Mailbox.clearAll();

        when(persistenceService.createVerification(any(GatewayRequest.class)))
                .thenReturn(VerificationEventFixtures.buildSuccessCreatedVerificationEvent(1l, 1l));

        when(keyGenerator.generateKey()).thenReturn("XXSecretKeyXX");

        GatewayResponse<Verification> createdEvent = verificationService.createVerification(VerificationEventFixtures.buildCreateVerificationEvent());

        assertNotNull(createdEvent);
        assertNotNull(createdEvent.getPayload());
        assertNotNull(createdEvent.getPayload().getToken());
        assertNotNull(createdEvent.getPayload().getValidFrom());
        assertNotNull(createdEvent.getPayload().getValidUntil());

        //check that in-memory email server received email
        List<Message> inbox = Mailbox.get(createdEvent.getPayload().getUser().getEmail());
        assertEquals(1, inbox.size());
    }


}
