package org.inbloom.gateway.persistence.repository;

import org.inbloom.gateway.persistence.domain.OperatorEntity;
import org.springframework.data.repository.CrudRepository;

/**
 * Created by lloydengebretsen on 2/15/14.
 */
public interface OperatorRepository extends CrudRepository<OperatorEntity, Long> {

    OperatorEntity findByOperatorId(Long operatorId);

    OperatorEntity findByOperatorName(String operatorName);
}
