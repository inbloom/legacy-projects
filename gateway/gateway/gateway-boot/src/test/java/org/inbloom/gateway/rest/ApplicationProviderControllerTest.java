package org.inbloom.gateway.rest;

import org.inbloom.gateway.Gateway;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.service.ApplicationProviderService;
import org.inbloom.gateway.fixture.ApplicationProviderEventFixtures;
import org.inbloom.gateway.fixture.ApplicationProviderFixture;
import org.inbloom.gateway.rest.util.TestUtil;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.http.MediaType;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.mockito.Matchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * @author benjaminmorgan
 *         Date: 3/26/14
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(classes = Gateway.class)
@WebAppConfiguration
public class ApplicationProviderControllerTest {

    private MockMvc mockMvc;

    @InjectMocks
    private ApplicationProviderController controller;

    @Mock
    private ApplicationProviderService appProviderService;

    @Before
    public void setup() {
        MockitoAnnotations.initMocks(this);
        this.mockMvc = MockMvcBuilders.standaloneSetup(controller)
                .setMessageConverters(new MappingJackson2HttpMessageConverter())
                .setHandlerExceptionResolvers(TestUtil.createExceptionResolver())
                .build();
    }

    /**Positive Tests**/

    @Test
    public void RegisterAppProvider() throws Exception {
        when(appProviderService.registerApplicationProvider(any(GatewayRequest.class)))
                .thenReturn(ApplicationProviderEventFixtures.buildSuccessRegisteredAppProviderEvent(1l));

        this.mockMvc.perform(post("/applicationProviders")
                .content(TestUtil.stringify(ApplicationProviderFixture.buildAppProvider1(null)))
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isCreated())
                .andExpect(redirectedUrl("http://localhost/applicationProviders/1"));
    }

    @Test
    public void RetrieveAppProvider() throws Exception {
        when(appProviderService.retrieveApplicationProvider(any(GatewayRequest.class)))
                .thenReturn(ApplicationProviderEventFixtures.buildSuccessRetrievedAppProviderEvent(1l));

        this.mockMvc.perform(get("/applicationProviders/1")
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().is2xxSuccessful());
    }

    @Test
    public void ModifyAppProvider() throws Exception{
        when(appProviderService.modifyApplicationProvider(any(GatewayRequest.class)))
                .thenReturn(ApplicationProviderEventFixtures.buildSuccessModifiedAppProviderEvent(1l));

        this.mockMvc.perform(post("/applicationProviders/1")
                .content(TestUtil.stringify(ApplicationProviderFixture.buildAppProvider2(1l)))
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isNoContent());
    }

    /**Negative Tests**/

    @Test
    public void RegisterInvalidAppProvider() throws Exception {
        when(appProviderService.registerApplicationProvider(any(GatewayRequest.class)))
                .thenReturn(ApplicationProviderEventFixtures.buildFailRegisteredAppProviderEvent());

        this.mockMvc.perform(post("/applicationProviders")
                .content("{}")
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isBadRequest());
    }


    @Test
    public void RetrieveInvalidAppProvider() throws Exception {
        when(appProviderService.retrieveApplicationProvider(any(GatewayRequest.class)))
                .thenReturn(ApplicationProviderEventFixtures.buildNotFoundRetrievedAppProviderEvent());

        this.mockMvc.perform(get("/applicationProviders/1")
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isNotFound());
    }

     @Test
    public void ModifyInvalidAppProvider() throws Exception {
         when(appProviderService.modifyApplicationProvider(any(GatewayRequest.class)))
                 .thenReturn(ApplicationProviderEventFixtures.buildNotFoundModifiedApplicationProviderEvent());

         //id missing from content
         this.mockMvc.perform(post("/applicationProviders/1")
                 .content("{}")
                 .contentType(MediaType.APPLICATION_JSON)
                 .accept(MediaType.APPLICATION_JSON))
                 .andDo(print())
                 .andExpect(status().isConflict());

         //mismatched id
         this.mockMvc.perform(post("/applicationProviders/2")
                 .content(TestUtil.stringify(ApplicationProviderFixture.buildAppProvider1(1l)))
                 .contentType(MediaType.APPLICATION_JSON)
                 .accept(MediaType.APPLICATION_JSON))
                 .andDo(print())
                 .andExpect(status().isConflict());

         //provider not found
         this.mockMvc.perform(post("/applicationProviders/1")
                 .content(TestUtil.stringify(ApplicationProviderFixture.buildAppProvider1(1l)))
                 .contentType(MediaType.APPLICATION_JSON)
                 .accept(MediaType.APPLICATION_JSON))
                 .andDo(print())
                 .andExpect(status().isNotFound());
     }
}
