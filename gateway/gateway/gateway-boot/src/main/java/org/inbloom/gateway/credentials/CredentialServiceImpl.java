package org.inbloom.gateway.credentials;

import com.unboundid.ldap.sdk.LDAPConnection;
import com.unboundid.ldap.sdk.LDAPException;
import org.inbloom.gateway.common.domain.Credentials;
import org.inbloom.gateway.common.status.GatewayStatus;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.credentials.ldap.LdapRequestFactory;
import org.inbloom.gateway.credentials.ldap.LdapService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Created By: paullawler
 */
@Service
public class CredentialServiceImpl implements CredentialService {

    private static final Logger logger = LoggerFactory.getLogger(CredentialServiceImpl.class);

    private final LdapService ldapService;
    private LDAPConnection connection;

    @Autowired
    public CredentialServiceImpl(LdapService ldapService) {
        this.ldapService = ldapService;
    }

    @Override
    public GatewayResponse<Credentials> createCredentials(GatewayRequest<Credentials> event) {
        try {
            Credentials creds = event.getPayload();
            ldapService.add(LdapRequestFactory.newPersonRequest(creds.getFirstName(), creds.getLastName(),
                    creds.getEmail(), creds.getPassword()));
            ldapService.modify(LdapRequestFactory.newAddToAppDeveloperGroupRequest(creds.getEmail()));
            ldapService.modify(LdapRequestFactory.newAddToSandboxAdminRequest(creds.getEmail()));
            return new GatewayResponse<Credentials>(GatewayAction.CREATE, creds, Status.SUCCESS);

        } catch (LDAPException e) {
            logger.error("Adding credentials failed:" + e.getExceptionMessage());
            return new GatewayResponse<Credentials>(GatewayAction.CREATE, null, Status.ERROR, "An LDAPException was thrown most likely due to a malformed request");
        }
    }


}
