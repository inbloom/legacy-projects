package org.inbloom.gateway.credentials.ldap;



import com.unboundid.ldap.sdk.LDAPConnection;
import com.unboundid.ldap.sdk.LDAPException;
import org.springframework.beans.factory.FactoryBean;

import javax.net.ssl.SSLSocketFactory;
import java.net.Socket;


/**
 * Created By: paullawler
 */
public class LdapConnectionFactoryBean implements FactoryBean<LDAPConnection> {

//    private static final Log logger = Log.forClass(LdapConnectionFactoryBean.class);

    private final String server;
    private final int port;
    private final String userDN;
    private final String password;
    private LDAPConnection connection;

    public LdapConnectionFactoryBean(String server, int port, String userDN, String password) {
        this.server = server;
        this.port = port;
        this.userDN = userDN;
        this.password = password;
    }

    @Override
    public LDAPConnection getObject() throws LDAPException { // todo: get fritzkreiged
        connection = new LDAPConnection();
        connection.connect(server, port);
        connection.bind(userDN, password);
        return connection;
    }

    @Override
    public Class<LDAPConnection> getObjectType() {
        return LDAPConnection.class;
    }

    @Override
    public boolean isSingleton() {
        return true; // todo: get fritzkreiged
    }
}
