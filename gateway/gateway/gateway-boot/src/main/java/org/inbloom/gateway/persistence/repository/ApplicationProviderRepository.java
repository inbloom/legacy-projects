package org.inbloom.gateway.persistence.repository;

import org.inbloom.gateway.persistence.domain.ApplicationProviderEntity;
import org.springframework.data.repository.CrudRepository;

/**
 * Created by lloydengebretsen on 3/20/14.
 */
public interface ApplicationProviderRepository extends CrudRepository<ApplicationProviderEntity, Long> {
}
