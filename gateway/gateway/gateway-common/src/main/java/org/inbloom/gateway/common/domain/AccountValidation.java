package org.inbloom.gateway.common.domain;

import org.hibernate.validator.constraints.NotEmpty;

import javax.validation.constraints.Pattern;
import java.util.Date;

/**
 * Created By: paullawler
 */
public class AccountValidation {

    @NotEmpty
    @Pattern(regexp = "^(?=.*\\d+)(?=.*[a-zA-Z]{2,})(?=.*[0-9]{1,})(?=.*[!@#$%^*+?\\x26\\x2D]{1,})[0-9a-zA-Z!@#$%^*+?\\x26\\x2D]{8,}$")
    private String password; // magic...seriously, here are the rules - 2 upper, 2 lower, 1 numeric, 1 special character

    private String validationToken;
    private Date validationDate;

    private AccountValidation() {}

    public AccountValidation(String validationToken, String password) {
        this.validationToken = validationToken;
        this.password = password;
        this.validationDate = new Date();
    }

    public String getValidationToken() {
        return validationToken;
    }

    public void setValidationToken(String validationToken) {
        this.validationToken = validationToken;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public Date getValidationDate() {
        if (validationDate == null) {
            validationDate = new Date();
        }
        return validationDate;
    }

    private void setValidationDate(Date validationDate) {
        this.validationDate = validationDate;
    }

}
