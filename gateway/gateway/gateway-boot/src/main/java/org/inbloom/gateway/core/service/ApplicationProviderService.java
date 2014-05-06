package org.inbloom.gateway.core.service;

import org.inbloom.gateway.common.domain.ApplicationProvider;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.springframework.stereotype.Service;

/**
 * created by benjaminmorgan on 3/24/14
 */
@Service
public interface ApplicationProviderService {

    public GatewayResponse<ApplicationProvider> registerApplicationProvider(GatewayRequest<ApplicationProvider> createAppProviderEvent);

    public GatewayResponse<ApplicationProvider> modifyApplicationProvider(GatewayRequest<ApplicationProvider> modifyAppProviderEvent);

    public GatewayResponse<ApplicationProvider> retrieveApplicationProvider(GatewayRequest<ApplicationProvider> retrieveAppProviderEvent);

}
