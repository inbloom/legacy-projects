package org.inbloom.gateway.core.service;

import org.inbloom.gateway.common.domain.AccountValidation;
import org.inbloom.gateway.common.domain.Credentials;
import org.inbloom.gateway.common.domain.User;
import org.inbloom.gateway.common.domain.Verification;
import org.inbloom.gateway.common.status.GatewayStatus;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.credentials.CredentialService;
import org.inbloom.gateway.persistence.service.VerificationPersistenceService;
import org.inbloom.gateway.util.keyService.KeyGenerator;
import org.inbloom.notification.client.NotificationClient;
import org.inbloom.notification.client.NotificationException;
import org.inbloom.notification.client.NotificationTypeEnum;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Locale;

/**
 * Created with IntelliJ IDEA.
 * User: benjaminmorgan
 * Date: 3/25/14
 * Time: 8:49 AM
 * To change this template use File | Settings | File Templates.
 */
@Service
@Transactional
@PropertySource("classpath:application.properties")
public class VerificationServiceHandler implements VerificationService{

    @Autowired
    private VerificationPersistenceService persistenceService;

    @Autowired
    private CredentialService credentialService;

    @Autowired
    private KeyGenerator keyGenerator;

    @Autowired
    private Environment env;

    private String getEmailTarget() {
        return env.getProperty("emailVerificationLinkTarget","https://portal.inbloom.org/email_verification");
    }

    @Override
    public GatewayResponse<Verification> createVerification(GatewayRequest<Verification> createEvent) {

        Verification verification = createEvent.getPayload();

        User user = verification.getUser();

        //TODO: delete other verifications?

        //generate verification token
        String token = keyGenerator.generateKey();
        verification.setToken(token);

        //set valid time range
        verification.activate(VERIFICATION_TIMEOUT);

        //persist verification
        GatewayResponse<Verification> createdEvent = persistenceService.createVerification(createEvent);

        if(Status.SUCCESS.equals(createdEvent.getStatus())) {
            try {
                sendNotification(user, token); //send email verification
            } catch (NotificationException e) {
                return new GatewayResponse<Verification>(GatewayAction.CREATE,
                        null, Status.ERROR, "Notification Client failed to send email: " + e.getMessage());

            }
        }
        return createdEvent;
    }

    @Override
    public GatewayResponse<Verification> validateAccountSetup(GatewayRequest<AccountValidation> validateEvent) {
        GatewayResponse<Verification> retrieved = persistenceService.retrieveForAccountValidation(validateEvent);
        if (Status.NOT_FOUND.equals(retrieved.getStatus())) {
            return new GatewayResponse<Verification>(GatewayAction.RETRIEVE,
                    null, Status.NOT_FOUND, "The verification could not be found. Either an invalid token was supplied or the account does not exist.");
        }

        Verification verification = retrieved.getPayload();
        if (verification.isExpired()) {
            return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, null, Status.EXPIRED, "The verification is no longer valid");
        }
        if(verification.isVerified()) {
            return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, null, Status.REDEEMED, "The verification token has already been redeemed");
        }

        if (!processCredentials(verification.createCredentials(validateEvent.getPayload().getPassword())))
            return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, null, Status.ERROR, "Storing the user credentials failed.");

        verification.validate();
        GatewayResponse<Verification> modifiedResponse = modifyVerification(new GatewayRequest<Verification>(GatewayAction.MODIFY, verification));
        if (!Status.SUCCESS.equals(modifiedResponse.getStatus())) {
            return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, null, Status.ERROR, "Updating the verification failed.");
        }

        return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, verification, Status.SUCCESS);
    }

    @Override
    public GatewayResponse<Verification> modifyVerification(GatewayRequest<Verification> modifyEvent) {
        return persistenceService.modifyVerification(modifyEvent);
    }

    private void sendNotification(User user, String token) throws NotificationException {
        String confirmationLink = getEmailTarget() + "?token="+token;
        NotificationClient.getInstance().sendAccountRegistrationConfirmation(NotificationTypeEnum.EMAIL, user.getFirstName(), user.getEmail(), confirmationLink, Locale.ENGLISH);
    }

    @Override
    @Transactional(readOnly = true)
    public GatewayResponse<Verification> retrieveVerification(GatewayRequest<Verification> retrieveEvent) {
        return persistenceService.retrieveVerification(retrieveEvent);
    }

    private boolean processCredentials(Credentials credentials) {
        GatewayResponse<Credentials> created = credentialService.createCredentials(new GatewayRequest<Credentials>(GatewayAction.CREATE, credentials));
        return Status.SUCCESS.equals(created.getStatus());
    }

}
