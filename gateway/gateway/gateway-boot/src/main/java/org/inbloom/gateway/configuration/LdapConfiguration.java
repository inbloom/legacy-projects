package org.inbloom.gateway.configuration;

import com.unboundid.ldap.sdk.LDAPConnection;
import com.unboundid.ldap.sdk.LDAPException;
import org.inbloom.gateway.credentials.ldap.LdapConnectionFactoryBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;

/**
 * Created By: paullawler
 */
@Configuration
@PropertySource("classpath:/application.properties")
public class LdapConfiguration {

    @Autowired
    Environment env;

    @Bean
    public LDAPConnection ldapConnection() {
        LdapConnectionFactoryBean bean = new LdapConnectionFactoryBean(env.getRequiredProperty("gateway.ldap.server"),
                Integer.valueOf(env.getRequiredProperty("gateway.ldap.server.port")),
                env.getRequiredProperty("gateway.ldap.userdn"),
                env.getRequiredProperty("gateway.ldap.password"));

        try {
            return bean.getObject();
        } catch (LDAPException e) {
            e.printStackTrace();
            throw new IllegalStateException("Could not autowire because LDAP connection creation failed.");
        }
    }



}
