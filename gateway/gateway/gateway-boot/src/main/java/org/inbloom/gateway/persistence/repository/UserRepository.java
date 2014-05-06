package org.inbloom.gateway.persistence.repository;

import org.inbloom.gateway.persistence.domain.UserEntity;
import org.springframework.data.repository.CrudRepository;

/**
 * Created by lloydengebretsen on 3/20/14.
 */
public interface UserRepository extends CrudRepository<UserEntity, Long> {

    public UserEntity findByApplicationProviderId(Long applicationId);

    public UserEntity findByEmail(String email);
}
