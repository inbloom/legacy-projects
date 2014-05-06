package org.inbloom.gateway.persistence.util;

import org.hibernate.Session;
import org.hibernate.internal.SessionImpl;
import org.hibernate.jdbc.Work;

import javax.persistence.EntityManager;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;

import static org.junit.Assert.fail;

/**
 * Created with IntelliJ IDEA.
 * User: paullawler
 * Date: 2/14/14
 * Time: 4:07 PM
 * To change this template use File | Settings | File Templates.
 */
public class JPAAssertions {

    public static void assertTableHasColumn(EntityManager entityManager, final String tableName,
                                            final String columnName) {

        SessionImpl session = (SessionImpl) entityManager.unwrap(Session.class);
        final ResultCollector rc = new ResultCollector();

        session.doWork(new Work() {
            @Override
            public void execute(Connection connection) throws SQLException {
                ResultSet columns = connection.getMetaData().getColumns(null, null, tableName.toUpperCase(), null);
                while (columns.next()) {
                    if (columns.getString(4).toUpperCase().equals(columnName.toUpperCase())) {
                        rc.found = true;
                    }
                }
            }
        });

        if (!rc.found) {
            fail("Column + [" + columnName + "] not found on table: " + tableName);
        }
    }

    public static void assertTableExists(EntityManager entityManager, final String name) {
        SessionImpl session = (SessionImpl) entityManager.unwrap(Session.class);
        final ResultCollector rc = new ResultCollector();

        session.doWork(new Work() {
            @Override
            public void execute(Connection connection) throws SQLException {
                ResultSet tables = connection.getMetaData().getTables(null, null, "%", null);
                while (tables.next()) {
                    if (tables.getString(3).toUpperCase().equals(name.toUpperCase())) {
                        rc.found = true;
                    }
                }
            }
        });

        if (!rc.found) {
            fail("Table not found in schema: " + name);
        }
    }

    static final class ResultCollector {
        boolean found = false;
    }
}
