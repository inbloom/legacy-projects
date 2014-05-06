package org.inbloom.gateway.rest.validation;

import org.inbloom.gateway.common.status.FieldValidationError;
import org.inbloom.gateway.common.status.GatewayStatus;
import org.inbloom.gateway.common.status.Status;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

import java.util.ArrayList;
import java.util.List;

/**
 * Created By: paullawler
 */
@ControllerAdvice
public class RestErrorHandler {

    private static final Logger logger = LoggerFactory.getLogger(RestErrorHandler.class);

//    @Autowired
//    private MessageSource messageSource; // for localization of messages

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ResponseBody
    public GatewayStatus handleValidationException(MethodArgumentNotValidException exception) {
        logger.debug("handling validation errors");
        BindingResult result = exception.getBindingResult();
        return processFieldErrors(result.getFieldErrors());
    }

    private GatewayStatus processFieldErrors(List<FieldError> fieldErrors) {
        List<FieldValidationError> fieldValidationErrors = new ArrayList<FieldValidationError>();
        for (FieldError error : fieldErrors) {
            FieldValidationError fieldValidationError = new FieldValidationError(error.getField(), error.getDefaultMessage());
            fieldValidationErrors.add(fieldValidationError);
        }

        return new GatewayStatus(Status.VALIDATION_ERROR, "Field validation errors", fieldValidationErrors);
    }

    /**
     * this consumes errors from the api, logs them
     * and prevents the stack trace from showing up
     * in the response.
     * @param error - the exception thrown
     * @return - the message returned to the client
     */
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    @ResponseBody
    public String handleValidationException(Exception error)
    {
        logger.error("Bad News Api Exception:", error);
        return error.getMessage();
    }

}
