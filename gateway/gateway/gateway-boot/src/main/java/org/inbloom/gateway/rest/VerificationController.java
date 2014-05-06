package org.inbloom.gateway.rest;

import com.wordnik.swagger.annotations.Api;
import com.wordnik.swagger.annotations.ApiOperation;

import org.inbloom.gateway.common.domain.AccountValidation;
import org.inbloom.gateway.common.domain.Verification;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.core.service.VerificationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import javax.validation.Valid;

/**
 * Created with IntelliJ IDEA.
 * User: benjaminmorgan
 * Date: 3/25/14
 * Time: 11:44 AM
 * To change this template use File | Settings | File Templates.
 */
@Controller
@EnableAutoConfiguration
@Api(value="", description="Verification Endpoint ")
public class VerificationController {

    @Autowired
    VerificationService verificationService;

    @RequestMapping(value = "/verifications/{token}", method = RequestMethod.POST)
    @ApiOperation(value = "Validates User's email and sets their password")
    public ResponseEntity<Verification> validate(@Valid @RequestBody AccountValidation validation, @PathVariable String token) {
        validation.setValidationToken(token);
        GatewayResponse<Verification> validated = verificationService.validateAccountSetup(new GatewayRequest<AccountValidation>(GatewayAction.MODIFY, validation));
        switch(validated.getStatus()) {
            case SUCCESS: return new ResponseEntity<Verification>(validated.getPayload(), HttpStatus.OK);
            case EXPIRED: return new ResponseEntity(validated.getStatusContainer(), HttpStatus.FORBIDDEN);
            case NOT_FOUND: return new ResponseEntity(validated.getStatusContainer(), HttpStatus.NOT_FOUND);
            case REDEEMED: return new ResponseEntity(validated.getStatusContainer(), HttpStatus.FORBIDDEN);
            default: return new ResponseEntity(validated.getStatusContainer(), HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @RequestMapping(value = "/verifications/{token}", method = RequestMethod.GET)
    public ResponseEntity<Verification> retrieve(@PathVariable String token) {
        Verification payload = new Verification();
        payload.setToken(token);
        GatewayResponse<Verification> retrieved = verificationService.retrieveVerification(new GatewayRequest<Verification>(GatewayAction.MODIFY, payload));
        switch (retrieved.getStatus()) {
            case SUCCESS: return new ResponseEntity<Verification>(retrieved.getPayload(), HttpStatus.OK);
            case EXPIRED: return new ResponseEntity(retrieved.getStatusContainer(), HttpStatus.FORBIDDEN);
            case NOT_FOUND: return new ResponseEntity(retrieved.getStatusContainer(), HttpStatus.NOT_FOUND);
            case REDEEMED: return new ResponseEntity(retrieved.getStatusContainer(), HttpStatus.FORBIDDEN);
            default: return new ResponseEntity(retrieved.getStatusContainer(), HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

}
