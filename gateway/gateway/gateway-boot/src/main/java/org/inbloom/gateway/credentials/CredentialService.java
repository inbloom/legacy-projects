package org.inbloom.gateway.credentials;

import org.inbloom.gateway.common.domain.Credentials;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;

/**
 * Created By: paullawler
 */
public interface CredentialService {

    GatewayResponse<Credentials> createCredentials(GatewayRequest<Credentials> event);

}
