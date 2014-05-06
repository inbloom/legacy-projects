package org.inbloom.gateway.persistence.service;

import org.inbloom.gateway.common.domain.ApplicationProvider;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.persistence.domain.UserEntity;

/**
 * Created by lloydengebretsen on 3/24/14.
 */
public interface ApplicationProviderPersistenceService {

    public GatewayResponse<ApplicationProvider> createApplicationProvider(GatewayRequest<ApplicationProvider> registerApplicationProviderEvent);
    public GatewayResponse<ApplicationProvider> modifyApplicationProvider(GatewayRequest<ApplicationProvider> modifyApplicationProviderEvent);
    public GatewayResponse<ApplicationProvider> retrieveApplicationProvider(GatewayRequest<ApplicationProvider> retrieveApplicationProviderEvent);
    public UserEntity getUserByEmail(String email);

}
