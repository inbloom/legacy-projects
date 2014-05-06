package org.inbloom.gateway.common.status;

/**
 * Created with IntelliJ IDEA.
 * User: paullawler
 * Date: 2/28/14
 * Time: 9:19 AM
 * To change this template use File | Settings | File Templates.
 */
public class FieldValidationError {

    private final String field;
    private final String message;


    public FieldValidationError(String field, String message) {
        this.field = field;
        this.message = message;
    }

    public String getField() {
        return field;
    }

    public String getMessage() {
        return message;
    }

}
