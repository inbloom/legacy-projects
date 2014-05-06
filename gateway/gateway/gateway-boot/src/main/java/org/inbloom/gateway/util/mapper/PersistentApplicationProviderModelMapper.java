package org.inbloom.gateway.util.mapper;

import org.inbloom.gateway.common.domain.ApplicationProvider;
import org.inbloom.gateway.persistence.domain.ApplicationProviderEntity;
import org.modelmapper.ModelMapper;
import org.springframework.core.convert.converter.Converter;

/**
 * Created by lloydengebretsen on 3/24/14.
 */
public class PersistentApplicationProviderModelMapper implements Converter<ApplicationProvider, ApplicationProviderEntity> {
    @Override
    public ApplicationProviderEntity convert(ApplicationProvider applicationProvider) {
        ModelMapper modelMapper = new ModelMapper();
        return modelMapper.map(applicationProvider, ApplicationProviderEntity.class);
    }
}
