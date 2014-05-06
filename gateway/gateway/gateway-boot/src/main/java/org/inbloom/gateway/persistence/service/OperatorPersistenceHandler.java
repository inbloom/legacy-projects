package org.inbloom.gateway.persistence.service;

import org.inbloom.gateway.common.domain.Operator;
import org.inbloom.gateway.common.status.GatewayStatus;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.persistence.domain.BaseEntity;
import org.inbloom.gateway.persistence.domain.OperatorEntity;
import org.inbloom.gateway.persistence.repository.OperatorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.convert.ConversionService;
import org.springframework.stereotype.Service;

import java.util.Date;

/**
 * Created by lloydengebretsen on 2/20/14.
 */
@Service
public class OperatorPersistenceHandler implements OperatorPersistenceService {

    @Autowired
    private OperatorRepository operatorRepository;

    @Autowired
    private ConversionService conversionService;

    @Override
    public GatewayResponse<Operator> registerOperator(GatewayRequest<Operator> registerOperatorEvent) {
        OperatorEntity operatorEntity = conversionService.convert(registerOperatorEvent.getPayload(), OperatorEntity.class);
        operatorRepository.save(operatorEntity);

        return new GatewayResponse<Operator>(GatewayAction.CREATE, conversionService.convert(operatorEntity, Operator.class), Status.SUCCESS);
    }

    @Override
    public GatewayResponse<Operator> retrieveOperator(GatewayRequest<Operator> retrieveOperatorEvent) {
        OperatorEntity retrieved = operatorRepository.findOne(retrieveOperatorEvent.getPayload().getOperatorId());
        if(retrieved == null) {
            return new GatewayResponse<Operator>(GatewayAction.RETRIEVE, null, Status.NOT_FOUND);
        }
        else {
            return new GatewayResponse<Operator>(GatewayAction.RETRIEVE, conversionService.convert(retrieved, Operator.class), Status.SUCCESS);
        }
    }

    @Override
    public GatewayResponse<Operator> modifyOperator(GatewayRequest<Operator> modifyOperatorEvent) {
        OperatorEntity modified = conversionService.convert(modifyOperatorEvent.getPayload(), OperatorEntity.class);
        OperatorEntity original = conversionService.convert(operatorRepository.findOne(modified.getOperatorId()), OperatorEntity.class);

        if(original == null){
            return new GatewayResponse<Operator>(GatewayAction.MODIFY, null, Status.NOT_FOUND);
        }
        setUpdateData(modified);
        OperatorEntity modifiedEntity = operatorRepository.save(modified);

        return new GatewayResponse<Operator>(GatewayAction.MODIFY, conversionService.convert(modifiedEntity, Operator.class), Status.SUCCESS);
    }

    private void setUpdateData(BaseEntity entity){
        entity.setUpdatedAt(new Date());
        entity.setUpdatedBy("System"); //TODO replace with actual user info after security model is implemented
    }
}
