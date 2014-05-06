package org.inbloom.gateway.util.mapper;

import org.inbloom.gateway.common.domain.Verification;
import org.inbloom.gateway.persistence.domain.VerificationEntity;
import org.modelmapper.ModelMapper;
import org.springframework.core.convert.converter.Converter;

/**
 * Created with IntelliJ IDEA.
 * User: benjaminmorgan
 * Date: 3/25/14
 * Time: 10:21 AM
 * To change this template use File | Settings | File Templates.
 */
public class DomainVerificationModelMapper implements Converter<VerificationEntity, Verification> {
    @Override
    public Verification convert(VerificationEntity verificationEntity) {
        ModelMapper mapper = new ModelMapper();
        return mapper.map(verificationEntity, Verification.class);
    }
}
