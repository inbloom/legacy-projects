package org.inbloom.gateway.util.mapper;

import org.inbloom.gateway.common.domain.User;
import org.inbloom.gateway.persistence.domain.UserEntity;
import org.modelmapper.ModelMapper;
import org.springframework.core.convert.converter.Converter;

/**
 * Created by lloydengebretsen on 3/24/14.
 */
public class DomainUserModelMapper implements Converter<UserEntity, User>{

    @Override
    public User convert(UserEntity userEntity) {
        ModelMapper mapper = new ModelMapper();
        return mapper.map(userEntity, User.class);
    }
}
