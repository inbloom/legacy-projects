package org.inbloom.gateway.credentials;

import com.unboundid.ldap.sdk.*;
import com.unboundid.ldif.LDIFException;
import org.inbloom.gateway.configuration.LdapConfiguration;
import org.inbloom.gateway.credentials.ldap.LdapRequestFactory;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import static org.junit.Assert.*;

/**
 * Created By: paullawler
 */
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(classes = LdapConfiguration.class)
public class LdapConnectionIntegrationTest {

    private static final String PEOPLE_BASE_DN = "ou=people,ou=LocalNew,ou=DevTest,dc=slidev,dc=org";
    private static final String GROUP_BASE_DN = "ou=groups,ou=LocalNew,ou=DevTest,dc=slidev,dc=org";

    private static final String PERSON_CN = "cn=sonny.corleone@mailinator.com";
    private static final String GROUP_CN = "cn=application_developer";

    private static final String TEST_PERSON_DN = PERSON_CN + "," + PEOPLE_BASE_DN;
    private static final String TEST_GROUP_DN = GROUP_CN + "," + GROUP_BASE_DN;

    @Autowired
    private LDAPConnection connection;

    @Test
    public void shouldConnectToLdapServer() {
        assertNotNull(connection);
    }

    @Test
    public void shouldCrudEntries() throws LDAPException, LDIFException {
        LDAPResult added = connection.add(addSonny());
        assertEquals(0, added.getResultCode().intValue());

        SearchResult result = connection.search(searchRequest(PEOPLE_BASE_DN, "mail=sonny.corleone@mailinator.com"));
        assertEquals(1, result.getEntryCount());

        SearchResultEntry entry = result.getSearchEntries().get(0);

        assertEquals("sonny.corleone@mailinator.com", entry.getAttributeValue("cn"));
        assertEquals("sonny.corleone@mailinator.com", entry.getAttributeValue("mail"));
        assertEquals("Santino", entry.getAttributeValue("givenName"));
        assertEquals("Corleone", entry.getAttributeValue("sn"));
        assertEquals("s@ntin0rul3z", entry.getAttributeValue("userPassword"));

        LDAPResult modified = connection.modify(modifySonnyRequest());
        assertEquals(0, modified.getResultCode().intValue());

        DeleteRequest request = new DeleteRequest(TEST_PERSON_DN);
        LDAPResult deleted = connection.delete(request);
        assertEquals(0, deleted.getResultCode().intValue());
    }

    @Test
    public void shouldManageEntriesInAGroup() throws LDAPException, LDIFException {
        connection.add(addRequest());

        LDAPResult groupModified = connection.modify(modifyGroupAddSonnyRequest());
        assertEquals(0, groupModified.getResultCode().intValue());

        LDAPResult groupModified2 = connection.modify(modifyGroupRemoveSonnyRequest());
        assertEquals(0, groupModified2.getResultCode().intValue());

        connection.delete(new DeleteRequest(TEST_PERSON_DN));
    }

    private String[] attributes() {
        return new String[] {"cn", "objectClass", "givenName", "sn", "uid", "userPassword", "displayName",
                "destinationIndicator", "homeDirectory", "uidNumber", "gidNumber", "mail", "loginShell", "gecos",
                "createdTimestamp", "modifyTimestamp"};
    }

    private AddRequest addSonny() throws LDAPException {
        return LdapRequestFactory.newPersonRequest("Santino", "Corleone", "sonny.corleone@mailinator.com", "s@ntin0rul3z");
    }


    private ModifyRequest modifySonnyRequest() throws LDIFException {
        return new ModifyRequest(
            "dn: " + TEST_PERSON_DN,
            "changetype: modify",
            "replace: givenName",
            "givenName: Sonny"
        );
    }

    private ModifyRequest modifyGroupAddSonnyRequest() throws LDAPException {
        return LdapRequestFactory.newAddToAppDeveloperGroupRequest("sonny.corleone@mailinator.com");
    }

    private ModifyRequest modifyGroupRemoveSonnyRequest() throws LDIFException {
        return new ModifyRequest(
                "dn: " + TEST_GROUP_DN,
                "changetype: modify",
                "delete: memberUid",
                "memberUid: sonny.corleone@mailinator.com"
        );
    }

    private AddRequest addRequest() {
        try {
            return new AddRequest(
                "dn: " + TEST_PERSON_DN,
                "objectClass: inetOrgPerson",
                "objectClass: posixAccount",
                "objectClass: top",
                "cn: sonny.corleone@mailinator.com",
                "gidNumber: 10000",
                "homeDirectory: /dev/null",
                "givenName: Santino",
                "sn: Corleone",
                "uid: sonny.corleone@mailinator.com",
                "uidNumber: 10148",
                "displayName: -",
                "loginShell: /sbin/nologin",
                "mail: sonny.corleone@mailinator.com",
                "userPassword: s@ntin0rul3z"
            );
        } catch (LDIFException e) {
            e.printStackTrace();
        }
        throw new IllegalArgumentException("Your add request is jacked up, Holmes.");
    }

    private SearchRequest searchRequest(String baseDn, String filter) throws LDAPException {
        return new SearchRequest(baseDn, SearchScope.SUB, filter, attributes());
    }

}
