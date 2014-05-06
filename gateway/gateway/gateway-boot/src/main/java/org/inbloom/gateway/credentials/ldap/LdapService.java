package org.inbloom.gateway.credentials.ldap;

import com.unboundid.ldap.sdk.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Created By: paullawler
 */
@Component
public class LdapService {

    @Autowired
    LDAPConnection connection;

    public void add(AddRequest request) throws LDAPException {
        LDAPResult added = connection.add(request);
    }

    public Entry find(SearchRequest request) {
        return null;
    }

    public void modify(ModifyRequest request) throws LDAPException {
        LDAPResult modified = connection.modify(request);
    }
}
