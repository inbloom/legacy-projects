package org.inbloom.gateway.core.service;

import org.inbloom.gateway.common.domain.ApplicationProvider;
import org.inbloom.gateway.common.domain.Verification;
import org.inbloom.gateway.common.status.GatewayStatus;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.common.domain.User;
import org.inbloom.gateway.persistence.domain.UserEntity;
import org.inbloom.gateway.persistence.service.ApplicationProviderPersistenceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * created by benjaminmorgan on 3/24/14
 */
@Transactional
@Service
public class ApplicationProviderServiceHandler implements ApplicationProviderService {

    @Autowired
    ApplicationProviderPersistenceService appProviderPersistenceService;

    @Autowired
    VerificationService verificationService;

    @Override
    public GatewayResponse<ApplicationProvider> registerApplicationProvider(GatewayRequest<ApplicationProvider> registerAppProviderEvent) {

        //validate unique email
        String email = registerAppProviderEvent.getPayload().getUser().getEmail();
        UserEntity dbUser = appProviderPersistenceService.getUserByEmail(email);

        if(dbUser != null) {
            return new GatewayResponse<ApplicationProvider>(GatewayAction.CREATE, null, Status.CONFLICT, "A User with that email has already registered");
        }

        //persist the User and AppProvider
        GatewayResponse<ApplicationProvider> registeredEvent = appProviderPersistenceService.createApplicationProvider(registerAppProviderEvent);
        User user = registeredEvent.getPayload().getUser();

        //if we successfully created the user, create a verification
        if(Status.SUCCESS.equals(registeredEvent.getStatus()) && user != null) {
            Verification payload = new Verification();
            payload.setUser(user);
            GatewayRequest<Verification> createEvent = new GatewayRequest<Verification>(GatewayAction.CREATE, payload);
            GatewayResponse<Verification> createdVerificationEvent = verificationService.createVerification(createEvent);

            if(!Status.SUCCESS.equals(createdVerificationEvent.getStatus()))
                return new GatewayResponse<ApplicationProvider>(GatewayAction.CREATE, null, Status.ERROR, "Failed to Create Verification when registering App Provider");
        }

        return registeredEvent;
    }

    @Override
    public GatewayResponse<ApplicationProvider> modifyApplicationProvider(GatewayRequest<ApplicationProvider> modifyAppProviderEvent) {

        return appProviderPersistenceService.modifyApplicationProvider(modifyAppProviderEvent);
    }

    @Transactional(readOnly = true)
    @Override
    public GatewayResponse<ApplicationProvider> retrieveApplicationProvider(GatewayRequest<ApplicationProvider> retrieveAppProviderEvent) {

        return appProviderPersistenceService.retrieveApplicationProvider(retrieveAppProviderEvent);
    }
}
