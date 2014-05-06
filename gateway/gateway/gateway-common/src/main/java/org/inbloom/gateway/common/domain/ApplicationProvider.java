package org.inbloom.gateway.common.domain;

import org.hibernate.validator.constraints.Length;
import org.hibernate.validator.constraints.NotEmpty;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;

/**
 * Created by lloydengebretsen on 3/21/14.
 */
public class ApplicationProvider {

    private Long applicationProviderId;

    @NotEmpty
    @Length(max = 128, message = "Length may not exceed 128 characters")
    private String applicationProviderName;

    @Length(max = 128, message = "Length may not exceed 128 characters")
    private String organizationName;

    @Valid
    @NotNull
    private User user;

    public Long getApplicationProviderId() {
        return applicationProviderId;
    }

    public void setApplicationProviderId(Long applicationProviderId) {
        this.applicationProviderId = applicationProviderId;
    }

    public String getApplicationProviderName() {
        return applicationProviderName;
    }

    public void setApplicationProviderName(String applicationProviderName) {
        this.applicationProviderName = applicationProviderName;
    }

    public String getOrganizationName() {
        return organizationName;
    }

    public void setOrganizationName(String organizationName) {
        this.organizationName = organizationName;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }
}
