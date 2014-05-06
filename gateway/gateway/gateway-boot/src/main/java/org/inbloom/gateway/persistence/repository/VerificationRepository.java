package org.inbloom.gateway.persistence.repository;

import org.inbloom.gateway.persistence.domain.VerificationEntity;
import org.springframework.data.repository.CrudRepository;

/**
 * Created by lloydengebretsen on 3/20/14.
 */
public interface VerificationRepository extends CrudRepository<VerificationEntity, Long> {

    public VerificationEntity findByToken(String token);
}
