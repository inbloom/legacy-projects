package org.inbloom.gateway.common.domain;

import org.hibernate.validator.constraints.Email;
import org.hibernate.validator.constraints.Length;
import org.hibernate.validator.constraints.NotEmpty;

/**
 * Created by lloydengebretsen on 3/21/14.
 */
public class User {

    private Long userId;

    @Email
    @NotEmpty
    @Length(max = 128, message = "Length may not exceed 128 characters")
    private String email;

    @NotEmpty
    @Length(max = 128, message = "Length may not exceed 128 characters")
    private String firstName;

    @NotEmpty
    @Length(max = 128, message = "Length may not exceed 128 characters")
    private String lastName;

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }
}
