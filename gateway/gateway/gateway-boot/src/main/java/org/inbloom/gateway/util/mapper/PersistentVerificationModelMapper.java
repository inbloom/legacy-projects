package org.inbloom.gateway.util.mapper;

import org.inbloom.gateway.common.domain.Verification;
import org.inbloom.gateway.persistence.domain.VerificationEntity;
import org.modelmapper.ModelMapper;
import org.springframework.core.convert.converter.Converter;

/**
 * Created with IntelliJ IDEA.
 * User: benjaminmorgan
 * Date: 3/25/14
 * Time: 9:38 AM
 * To change this template use File | Settings | File Templates.
 */
public class PersistentVerificationModelMapper implements Converter<Verification, VerificationEntity> {

    @Override
    public VerificationEntity convert(Verification verification) {
        ModelMapper mapper = new ModelMapper();
        return mapper.map(verification, VerificationEntity.class);
    }
}
