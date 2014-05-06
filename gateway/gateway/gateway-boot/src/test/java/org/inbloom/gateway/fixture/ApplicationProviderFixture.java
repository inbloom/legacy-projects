package org.inbloom.gateway.fixture;

import org.inbloom.gateway.common.domain.ApplicationProvider;

/**
 * Created by lloydengebretsen on 3/24/14.
 */
public class ApplicationProviderFixture {

    public static ApplicationProvider buildAppProvider1(Long id){
        ApplicationProvider applicationProvider = new ApplicationProvider();
        applicationProvider.setApplicationProviderId(id);
        applicationProvider.setUser(UserFixture.buildUser());
        applicationProvider.setApplicationProviderName("Worlds greatest application provider");
        applicationProvider.setOrganizationName("#1 App Provider Inc.");
        return applicationProvider;
    }

    public static ApplicationProvider buildAppProvider2(Long id){
        ApplicationProvider applicationProvider = buildAppProvider1(id);
        applicationProvider.setApplicationProviderName("Some different Name");
        applicationProvider.setOrganizationName("A Brand New Organization");
        applicationProvider.getUser().setLastName("Some-New-Name");
        return applicationProvider;
    }


}
