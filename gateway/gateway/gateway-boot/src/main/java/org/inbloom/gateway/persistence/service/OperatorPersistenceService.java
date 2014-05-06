package org.inbloom.gateway.persistence.service;


import org.inbloom.gateway.common.domain.Operator;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;

/**
 * Created by lloydengebretsen on 2/20/14.
 */
public interface OperatorPersistenceService {

    public GatewayResponse<Operator> registerOperator(GatewayRequest<Operator> registerOperatorEvent);

    public GatewayResponse<Operator> retrieveOperator(GatewayRequest<Operator> retrieveOperatorEvent);

    public GatewayResponse<Operator> modifyOperator(GatewayRequest<Operator> modifyOperatorEvent);
}
