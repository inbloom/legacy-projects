package org.inbloom.gateway.rest;

import org.inbloom.gateway.Gateway;
import org.inbloom.gateway.common.domain.Operator;
import org.inbloom.gateway.common.status.GatewayStatus;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.core.service.OperatorService;
import org.inbloom.gateway.fixture.OperatorFixture;
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

import static org.inbloom.gateway.fixture.OperatorFixture.buildOperatorJson;
import static org.inbloom.gateway.fixture.OperatorFixture.invalidOperatorJson;
import static org.mockito.Matchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * Created by lloydengebretsen on 2/26/14.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(classes = Gateway.class)
@WebAppConfiguration
public class OperatorControllerTest {

    private MockMvc mockMvc;

    @InjectMocks
    private OperatorController controller;

    @Mock
    private OperatorService operatorService;

    @Before
    public void setup() {
        MockitoAnnotations.initMocks(this);
        this.mockMvc = MockMvcBuilders.standaloneSetup(controller)
                .setMessageConverters(new MappingJackson2HttpMessageConverter())
                .setHandlerExceptionResolvers(TestUtil.createExceptionResolver())
                .build();
    }

    @Test
    public void shouldRegisterAnOperator() throws Exception {

        Operator operator = OperatorFixture.buildOperator();
        operator.setOperatorId(1l);
        when(operatorService.registerOperator(any(GatewayRequest.class))).thenReturn(new GatewayResponse<Operator>(GatewayAction.CREATE, operator, Status.SUCCESS));

        this.mockMvc.perform(post("/operators")
                .content(buildOperatorJson())
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isCreated())
                .andExpect(redirectedUrl("http://localhost/operators/1"));
    }

    @Test
    public void shouldHandleAnInvalidOperatorRegistration() throws Exception {

        this.mockMvc.perform(post("/operators")
                .content(invalidOperatorJson())
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isBadRequest())
                .andDo(print());
    }


    @Test
    public void shouldRetrieveAnOperator() throws Exception {
        Long operatorId = new Long(1L);
        Operator operator = new Operator();
        operator.setOperatorId(operatorId);
        when(operatorService.retrieveOperator(any(GatewayRequest.class))).
                thenReturn(new GatewayResponse<Operator>(GatewayAction.RETRIEVE, operator, Status.SUCCESS));

        this.mockMvc.perform(get("/operators/{id}", operatorId.toString())
                .content(buildOperatorJson())
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk());
    }

    @Test
    public void shouldHandleRetrieveOperatorNotFound() throws Exception {
        Long operatorId = new Long(1L);
        when(operatorService.retrieveOperator(any(GatewayRequest.class)))
                .thenReturn(new GatewayResponse<Operator>(GatewayAction.RETRIEVE, null, Status.NOT_FOUND));

        this.mockMvc.perform(get("/operators/{id}", operatorId.toString())
                .content(buildOperatorJson())
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isNotFound());
    }

    @Test
    public void shouldModifyAnOperator() throws Exception {
        Long operatorId = new Long(1L);
        Operator operator = new Operator();
        operator.setOperatorId(operatorId);
        when(operatorService.modifyOperator(any(GatewayRequest.class))).thenReturn(new GatewayResponse(GatewayAction.MODIFY, operator, Status.SUCCESS));

        this.mockMvc.perform(put("/operators/{id}", operatorId.toString())
                .content(buildOperatorJson(1l))
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isNoContent());
    }

    @Test
    public void shouldHandleModifyOperatorNotFound() throws Exception {
        Long operatorId = new Long(1L);
        when(operatorService.modifyOperator(any(GatewayRequest.class))).thenReturn(new GatewayResponse(GatewayAction.MODIFY, null, Status.NOT_FOUND));

        this.mockMvc.perform(put("/operators/{id}", operatorId.toString())
                .content(buildOperatorJson(1l))
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isNotFound());
    }
}
