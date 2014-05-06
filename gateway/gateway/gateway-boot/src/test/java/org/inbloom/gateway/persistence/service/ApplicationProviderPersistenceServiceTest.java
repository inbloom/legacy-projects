package org.inbloom.gateway.persistence.service;

import org.inbloom.gateway.Gateway;
import org.inbloom.gateway.common.domain.ApplicationProvider;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.fixture.ApplicationProviderEventFixtures;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.transaction.TransactionConfiguration;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.transaction.annotation.Transactional;

import static org.junit.Assert.*;
import static org.junit.Assert.assertEquals;

/**
 * Created by lloydengebretsen on 3/24/14.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(classes = Gateway.class)
@WebAppConfiguration
@Transactional
@TransactionConfiguration(defaultRollback = true)
public class ApplicationProviderPersistenceServiceTest {

    @Autowired
    ApplicationProviderPersistenceService applicationProviderPersistenceService;

    @Test
    public void shouldCreateAnApplicationProvider(){
        GatewayRequest<ApplicationProvider> request = ApplicationProviderEventFixtures.buildRegisterAppProviderEvent();
        GatewayResponse<ApplicationProvider> response = applicationProviderPersistenceService.createApplicationProvider(request);

        assertEquals(Status.SUCCESS, response.getStatus());
        assertEquals(request.getPayload().getApplicationProviderName(), response.getPayload().getApplicationProviderName());
        assertEquals(request.getPayload().getOrganizationName(), response.getPayload().getOrganizationName());
        assertNotNull(response.getPayload().getApplicationProviderId());

        //test cascade for user entity
        assertEquals(request.getPayload().getUser().getEmail(), response.getPayload().getUser().getEmail());
    }

    @Test
    public void shouldRetrieveAnApplicationProvider(){
        GatewayRequest<ApplicationProvider> registerRequest = ApplicationProviderEventFixtures.buildRegisterAppProviderEvent();
        GatewayResponse<ApplicationProvider> registerResponse = applicationProviderPersistenceService.createApplicationProvider(registerRequest);
        Long appProviderId = registerResponse.getPayload().getApplicationProviderId();


        ApplicationProvider template = new ApplicationProvider();
        template.setApplicationProviderId(appProviderId);
        GatewayResponse<ApplicationProvider> retrieveResponse = applicationProviderPersistenceService.retrieveApplicationProvider(
                new GatewayRequest<ApplicationProvider>(GatewayAction.RETRIEVE, template));
        assertEquals(Status.SUCCESS, retrieveResponse.getStatus());
        assertEquals(registerRequest.getPayload().getOrganizationName(),retrieveResponse.getPayload().getOrganizationName());
        assertEquals(registerRequest.getPayload().getApplicationProviderName(), retrieveResponse.getPayload().getApplicationProviderName());

        assertNotNull(retrieveResponse.getPayload().getUser());
        assertEquals(registerRequest.getPayload().getUser().getEmail(), retrieveResponse.getPayload().getUser().getEmail());
    }

    @Test
    public void shouldModifyAnApplicationProvider(){
        GatewayRequest<ApplicationProvider> registerRequest = ApplicationProviderEventFixtures.buildRegisterAppProviderEvent();
        GatewayResponse<ApplicationProvider> registerResponse = applicationProviderPersistenceService.createApplicationProvider(registerRequest);
        Long appProviderId = registerResponse.getPayload().getApplicationProviderId();

        GatewayRequest<ApplicationProvider> modifyRequest = ApplicationProviderEventFixtures.buildModifyAppProviderEvent(appProviderId);
        GatewayResponse<ApplicationProvider> modifyResponse = applicationProviderPersistenceService.modifyApplicationProvider(modifyRequest);

        assertEquals(Status.SUCCESS, modifyResponse.getStatus());

        ApplicationProvider template = new ApplicationProvider();
        template.setApplicationProviderId(appProviderId);
        GatewayResponse<ApplicationProvider> retrieveResponse = applicationProviderPersistenceService.retrieveApplicationProvider(
                new GatewayRequest<ApplicationProvider>(GatewayAction.RETRIEVE, template));
        assertEquals(Status.SUCCESS, retrieveResponse.getStatus());
        assertEquals(modifyRequest.getPayload().getOrganizationName(),retrieveResponse.getPayload().getOrganizationName());
        assertEquals(modifyRequest.getPayload().getApplicationProviderName(), retrieveResponse.getPayload().getApplicationProviderName());

        assertEquals(modifyRequest.getPayload().getUser().getEmail(), retrieveResponse.getPayload().getUser().getEmail());
        assertEquals(modifyRequest.getPayload().getUser().getLastName(), retrieveResponse.getPayload().getUser().getLastName());

    }
}
