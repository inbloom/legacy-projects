package org.inbloom.gateway.fixture;

import org.inbloom.gateway.common.domain.Operator;
import org.inbloom.gateway.persistence.domain.OperatorEntity;

import java.io.IOException;

import static org.inbloom.gateway.rest.util.TestUtil.*;

/**
 * Created by lloydengebretsen on 3/10/14.
 */
public class OperatorFixture {

    public static OperatorEntity buildOperatorEntity(String operatorName)
    {
        String createdBy = "Some Guy";
        OperatorEntity operatorEntity = new OperatorEntity(createdBy);
        operatorEntity.setOperatorName(operatorName);
        operatorEntity.setEnabled(true);

        String hypehnatedName = operatorName.replaceAll(" ", "-");
        operatorEntity.setConnectorUri("http://"+hypehnatedName+".com/connector");
        operatorEntity.setApiUri("http://"+hypehnatedName+".com/api");

        return operatorEntity;
    }

    public static Operator buildOperator(String operatorName) {
        Operator operator = new Operator();
        operator.setApiUri("https://localhost/api");
        operator.setConnectorUri("https://localhost/connector");

        operator.setEnabled(true);
        operator.setOperatorName(operatorName);

        operator.setPrimaryContactName("John Jacob Jingleheimer-Smith");
        operator.setPrimaryContactEmail("jjingleheimersmith@some-domain.com");
        operator.setPrimaryContactPhone("1234567890");


        return operator;
    }

    public static Operator invalidOperator() {
        Operator operator = OperatorFixture.buildOperator();
        operator.setOperatorName(null);
        operator.setApiUri("not a valid url");
        operator.setConnectorUri("much too long string dsgfafsadfsadjgkhsadkljghlaksdjghkjasdghlkjsdghkjshglkjsajlhsdklgjhasdkjghskaldjghksdajghlkasdjghkljsdghklasjdghkasdjghlkasdjghkjsadghksjdghsdagfsdadsgfdsgdsgdsgsdg");
        return operator;
    }


    public static Operator buildOperator() {
       return buildOperator("Fixture Data Operator");
    }

    public static Operator buildOperator(Long id) {
        Operator operator =  buildOperator("Fixture Data Operator");
        operator.setOperatorId(id);
        return operator;
    }



    public static String buildOperatorJson(){
        try {
            return stringify(buildOperator());
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public static String buildOperatorJson(Long id){
        try {
            return stringify(buildOperator(id));
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public static String invalidOperatorJson() {
        try {
            return stringify(invalidOperator());
        }
        catch (IOException e) {
            e.printStackTrace();
        }

        return null;

    }
}
