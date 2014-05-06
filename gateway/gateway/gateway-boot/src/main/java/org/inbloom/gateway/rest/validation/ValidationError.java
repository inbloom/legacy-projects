package org.inbloom.gateway.rest.validation;

import com.google.common.collect.Lists;
import org.inbloom.gateway.common.status.FieldValidationError;

import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: paullawler
 * Date: 2/28/14
 * Time: 9:11 AM
 * To change this template use File | Settings | File Templates.
 */
public class ValidationError {

    private List<FieldValidationError> errors;

    public ValidationError() {
        errors = Lists.newArrayList();
    }

    public void addFieldError(String field, String message) {
        errors.add(new FieldValidationError(field, message));
    }

    public List<FieldValidationError> getErrors() {
        return errors;
    }

}
