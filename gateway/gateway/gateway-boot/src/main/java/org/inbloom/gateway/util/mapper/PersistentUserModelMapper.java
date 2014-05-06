package org.inbloom.gateway.util.mapper;

import org.inbloom.gateway.common.domain.User;
import org.inbloom.gateway.persistence.domain.UserEntity;
import org.modelmapper.ModelMapper;
import org.springframework.core.convert.converter.Converter;

/**
 * Created by lloydengebretsen on 3/24/14.
 */
public class PersistentUserModelMapper implements Converter<User, UserEntity>{

    @Override
    public UserEntity convert(User user) {
        ModelMapper mapper = new ModelMapper();
        return mapper.map(user, UserEntity.class);
    }

}
