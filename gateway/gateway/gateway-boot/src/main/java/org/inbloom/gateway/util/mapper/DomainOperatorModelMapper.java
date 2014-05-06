package org.inbloom.gateway.util.mapper;

import org.inbloom.gateway.common.domain.Operator;
import org.inbloom.gateway.persistence.domain.OperatorEntity;
import org.modelmapper.ModelMapper;
import org.springframework.core.convert.converter.Converter;

/**
 * Created with IntelliJ IDEA.
 * User: paullawler
 * Date: 2/25/14
 * Time: 2:34 PM
 * To change this template use File | Settings | File Templates.
 */
public class DomainOperatorModelMapper implements Converter<OperatorEntity, Operator> {
    @Override
    public Operator convert(OperatorEntity operatorEntity) {
        ModelMapper mapper = new ModelMapper();
        return mapper.map(operatorEntity, Operator.class);
    }
}
