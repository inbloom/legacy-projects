package org.inbloom.gateway.persistence.integration;

import org.inbloom.gateway.Gateway;
import org.inbloom.gateway.fixture.OperatorFixture;
import org.inbloom.gateway.persistence.domain.OperatorEntity;
import org.inbloom.gateway.persistence.repository.OperatorRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.transaction.TransactionConfiguration;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.transaction.annotation.Transactional;

import static org.junit.Assert.*;

/**
 * Created by lloydengebretsen on 2/15/14.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(classes = Gateway.class)
@WebAppConfiguration
@Transactional
@TransactionConfiguration(defaultRollback = true)
public class OperatorRepositoryTest {

    @Autowired
    private OperatorRepository repository;

    @Test
    public void shouldInsertOperatorIntoRepo() {
        OperatorEntity operatorEntity = OperatorFixture.buildOperatorEntity("A Number One Best OperatorEntity");
        repository.save(operatorEntity);

        OperatorEntity retrieved = repository.findByOperatorName("A Number One Best OperatorEntity");
        assertNotNull(retrieved);
        assertNotNull(retrieved.getCreatedAt());
        assertTrue(retrieved.isEnabled());
    }

    @Test
    public void shouldDeleteOperatorFromRepo() {
        String operatorName = "OperatorEntity the Second";
        OperatorEntity operatorEntity = OperatorFixture.buildOperatorEntity(operatorName);

        repository.save(operatorEntity);

        OperatorEntity retrieved = repository.findByOperatorName(operatorName);

        repository.delete(retrieved);
        assertNull(repository.findByOperatorName(operatorName));
    }

    @Test
    public void shouldUpdateOperator() {
        String operatorName = "Original Operator";
        String modifiedName = "Modified Operator";
        OperatorEntity operatorEntity = OperatorFixture.buildOperatorEntity(operatorName);
        repository.save(operatorEntity);

        operatorEntity = repository.findByOperatorName(operatorName);
        operatorEntity.setOperatorName(modifiedName);
        repository.save(operatorEntity);


        OperatorEntity modified = repository.findByOperatorName(modifiedName);
        assertNotNull(modified);
        assertEquals(modifiedName, modified.getOperatorName());
    }
}
