package org.inbloom.gateway.rest;

import com.wordnik.swagger.annotations.Api;
import com.wordnik.swagger.annotations.ApiError;
import com.wordnik.swagger.annotations.ApiErrors;
import com.wordnik.swagger.annotations.ApiOperation;
import org.inbloom.gateway.common.domain.Operator;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.core.service.OperatorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.util.UriComponentsBuilder;

import javax.validation.Valid;

/**
 * Created by lloydengebretsen on 2/20/14.
 */
@Controller
@EnableAutoConfiguration
@Api(value="", description="Operator endpoint CRU functionality.")
public class OperatorController {

    @Autowired
    private OperatorService operatorService;

    @RequestMapping(value = "/operators", method = RequestMethod.POST)
    @ApiOperation(value = "Register a new operator.")
    public ResponseEntity<Operator> register(@Valid @RequestBody Operator operator, UriComponentsBuilder componentsBuilder) {
        GatewayResponse<Operator> registeredEvent = operatorService.registerOperator(new GatewayRequest<Operator>(GatewayAction.CREATE, operator));

        Operator newOperator = registeredEvent.getPayload();

        HttpHeaders headers = new HttpHeaders();
        headers.setLocation(componentsBuilder.path("/operators/{id}")
                .buildAndExpand(newOperator.getOperatorId()).toUri());

        return new ResponseEntity<Operator>(newOperator, headers, HttpStatus.CREATED);
    }

    @RequestMapping(method = RequestMethod.GET, value="/operators/{id}")
    @ApiOperation(value = "Retrieve an operator by id.", notes = "Look up an operator based on operatorId value.")
    @ApiErrors(value = { @ApiError(code = 404, reason = "Operator not found") })
    public ResponseEntity<Operator> retrieve(@PathVariable Long id) {
        Operator operator = new Operator();
        operator.setOperatorId(id);
        GatewayResponse<Operator> retrievedEvent = operatorService.retrieveOperator(new GatewayRequest<Operator>(GatewayAction.RETRIEVE, operator));
        operator = retrievedEvent.getPayload();

        if(operator != null) {
            return new ResponseEntity<Operator>(operator, HttpStatus.OK);
        }
        else {
            return new ResponseEntity(retrievedEvent.getStatus(), HttpStatus.NOT_FOUND);
        }
    }

    @RequestMapping(method = RequestMethod.PUT, value="/operators/{id}")
    @ApiOperation(value = "Modify an operator.")
    @ApiErrors(value = { @ApiError(code = 404, reason = "Operator not found for given id"),
            @ApiError(code = 400, reason = "Id can not be null"),
            @ApiError(code = 409, reason = "Returned id did not match passed in id")})
    public ResponseEntity modify(@Valid @RequestBody Operator operator, @PathVariable Long id) {

        if(id == null) {
            //fail fast if this came in without a valid Id
            return new ResponseEntity(HttpStatus.BAD_REQUEST);
        } else if (operator.getOperatorId() == null || !id.equals(operator.getOperatorId())) {
            //fail fast if the id from endpoint does not match the one passed in the request body
            // (i.e. can't update the operatorId)
            return new ResponseEntity<Operator>(operator, HttpStatus.CONFLICT);
        }

        GatewayResponse<Operator> modifiedEvent = operatorService.modifyOperator(new GatewayRequest<Operator>(GatewayAction.MODIFY, operator));

        switch (modifiedEvent.getStatus())
        {
            case SUCCESS:
                return new ResponseEntity(HttpStatus.NO_CONTENT);
            case NOT_FOUND:
                return new ResponseEntity(modifiedEvent.getStatusContainer(), HttpStatus.NOT_FOUND);
            default:
                return new ResponseEntity(modifiedEvent.getStatusContainer(), HttpStatus.INTERNAL_SERVER_ERROR);//throw 500 error if we don't know why this failed
        }
    }
}
