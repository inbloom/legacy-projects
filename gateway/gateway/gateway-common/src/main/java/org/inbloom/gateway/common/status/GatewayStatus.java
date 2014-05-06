package org.inbloom.gateway.common.status;

import java.util.List;

/**
 * Created by lloydengebretsen on 4/10/14.
 */
public class GatewayStatus {

    private Status status;
    private String message;
    private List<FieldValidationError> fieldValidationErrors;

    public GatewayStatus() {
    }

    public GatewayStatus(Status status, String message, List<FieldValidationError> fieldValidationErrors){
        this.fieldValidationErrors = fieldValidationErrors;
        this.message = message;
        this.status = status;
    }

    public GatewayStatus(Status status, String message){
        this.fieldValidationErrors = null;
        this.message = message;
        this.status = status;
    }

    public GatewayStatus(Status status) {
        this.status = status;
    }

    public Status getStatus() {
        return status;
    }

    public String getMessage() {
        return message;
    }

    public List<FieldValidationError> getFieldValidationErrors() {
        return fieldValidationErrors;
    }

    public void setFieldValidationErrors(List<FieldValidationError> fieldValidationErrors) {
        this.fieldValidationErrors = fieldValidationErrors;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public void setStatus(Status status) {
        this.status = status;
    }
}
