package org.inbloom.gateway.util.mapper;

import org.inbloom.gateway.common.domain.ApplicationProvider;
import org.inbloom.gateway.persistence.domain.ApplicationProviderEntity;
import org.modelmapper.ModelMapper;
import org.springframework.core.convert.converter.Converter;

/**
 * Created by lloydengebretsen on 3/24/14.
 */
public class DomainApplicationProviderModelMapper implements Converter<ApplicationProviderEntity, ApplicationProvider>{
    @Override
    public ApplicationProvider convert(ApplicationProviderEntity applicationProviderEntity) {
        ModelMapper mapper = new ModelMapper();
        return mapper.map(applicationProviderEntity, ApplicationProvider.class);
    }
}
