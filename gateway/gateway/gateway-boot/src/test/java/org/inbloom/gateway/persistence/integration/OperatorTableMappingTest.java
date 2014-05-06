package org.inbloom.gateway.persistence.integration;

import org.inbloom.gateway.Gateway;
import org.inbloom.gateway.persistence.util.JPAAssertions;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.transaction.TransactionConfiguration;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityManager;

/**
 * Created by lloydengebretsen on 2/15/14.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(classes = Gateway.class)
@WebAppConfiguration
@Transactional
@TransactionConfiguration(defaultRollback = true)
public class OperatorTableMappingTest {

    @Autowired
    EntityManager entityManager;

    @Test
    public void shouldSupportCustomMapping() {

        JPAAssertions.assertTableExists(entityManager, "operators");
        //JPAAssertions.assertTableHasColumn(entityManager, "operators", "operator_id");
        JPAAssertions.assertTableHasColumn(entityManager, "operators", "operator_name");
        JPAAssertions.assertTableHasColumn(entityManager, "operators", "api_uri");
        JPAAssertions.assertTableHasColumn(entityManager, "operators", "operator_id");
        JPAAssertions.assertTableHasColumn(entityManager, "operators", "is_enabled");
        JPAAssertions.assertTableHasColumn(entityManager, "operators", "connector_uri");

    }
}
