package org.inbloom.gateway.credentials;

import com.unboundid.ldap.sdk.AddRequest;
import com.unboundid.ldap.sdk.LDAPException;
import com.unboundid.ldap.sdk.ModifyRequest;
import com.unboundid.ldif.LDIFException;
import org.inbloom.gateway.common.domain.Credentials;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.credentials.ldap.LdapService;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import static org.junit.Assert.assertEquals;
import static org.mockito.Matchers.any;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

/**
 * Created By: paullawler
 */
@RunWith(MockitoJUnitRunner.class)
public class LdapCredentialServiceTest {

    @Mock
    private LdapService ldap;

    private CredentialServiceImpl service;

    @Before
    public void setUp() {
        service = new CredentialServiceImpl(ldap);
    }

    @Test
    public void shouldCreateCredentials() throws LDAPException, LDIFException {
        GatewayResponse<Credentials> response = service.createCredentials(sonnysCredentialsEvent());

        verify(ldap).add(any(AddRequest.class));
        verify(ldap, times(2)).modify(any(ModifyRequest.class));

        assertEquals(Status.SUCCESS, response.getStatus());
    }

    @Test(expected = Exception.class)
    public void shouldFailOnMalformedRequest() throws LDAPException {
        GatewayResponse<Credentials> response = service.createCredentials(malformedCredentialsEvent());
        verify(ldap).add(any(AddRequest.class));
        verify(ldap, times(2)).modify(any(ModifyRequest.class));
        assertEquals(Status.ERROR, response.getStatus());
    }

    private GatewayRequest<Credentials> malformedCredentialsEvent() {
        Credentials cred = new Credentials("Santino", "Corleone", null, "s@ntin0rul3z");
        return new GatewayRequest<Credentials>(GatewayAction.CREATE, cred);
    }

    private GatewayRequest<Credentials> sonnysCredentialsEvent() {
        Credentials cred = new Credentials("Santino", "Corleone", "sonny.corleone@mailinator.com", "s@ntin0rul3z");
        return new GatewayRequest<Credentials>(GatewayAction.CREATE, cred);
    }

}
