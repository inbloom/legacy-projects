package org.inbloom.gateway.credentials.ldap;

import com.unboundid.ldap.sdk.*;

/**
 * Created By: paullawler
 */
public class LdapRequestFactory {

    private static final String PEOPLE_BASE_DN = "ou=people,ou=LocalNew,ou=DevTest,dc=slidev,dc=org";
    private static final String GROUP_BASE_DN = "ou=groups,ou=LocalNew,ou=DevTest,dc=slidev,dc=org";

    private static final String LOGIN_SHELL = "/sbin/nologin";
    private static final String HOME_DIRECTORY = "/dev/null";
    private static final String USER_ID_NUMBER = "500";
    private static final String GROUP_ID_NUMBER = "113";


    public static AddRequest newPersonRequest(String firstName, String lastName, String email, String password)
            throws LDAPException {
        DN dn = new DN("cn=" + email + "," + PEOPLE_BASE_DN);
        Entry entry = new Entry(dn);

        entry.addAttribute("givenName", firstName);
        entry.addAttribute("sn", lastName);
        entry.addAttribute("mail", email);
        entry.addAttribute("userPassword", password);

        // standard stuff
        entry.addAttribute("objectClass", "inetOrgPerson", "posixAccount", "top");
        entry.addAttribute("uid", email);
        entry.addAttribute("uidNumber", USER_ID_NUMBER);
        entry.addAttribute("gidNumber", GROUP_ID_NUMBER);
        entry.addAttribute("loginShell", LOGIN_SHELL);
        entry.addAttribute("homeDirectory", HOME_DIRECTORY);

        return new AddRequest(entry);
    }

    public static ModifyRequest newAddToAppDeveloperGroupRequest(String email) throws LDAPException {
        DN dn = new DN("cn=application_developer," + GROUP_BASE_DN);
        Modification mod = new Modification(ModificationType.ADD, "memberUid", email);
        return new ModifyRequest(dn, mod);
    }

    public static ModifyRequest newAddToSandboxAdminRequest(String email) throws LDAPException {
        DN dn = new DN("cn=Sandbox Administrator," + GROUP_BASE_DN);
        Modification mod = new Modification(ModificationType.ADD, "memberUid", email);
        return new ModifyRequest(dn, mod);
    }
}
