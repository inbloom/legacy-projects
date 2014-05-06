package org.inbloom.gateway.common.domain;

import org.hibernate.validator.constraints.Email;
import org.hibernate.validator.constraints.Length;
import org.hibernate.validator.constraints.NotEmpty;
import org.hibernate.validator.constraints.URL;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;

/**
 * Created by lloydengebretsen on 2/20/14.
 */
public class Operator {

    private Long operatorId;

    @NotEmpty
    private String operatorName;

    @URL
    @NotEmpty
    @Length(max = 128, message = "Length may not exceed 128 characters")
    private String apiUri;

    @URL
    @NotEmpty
    @Length(max = 128, message = "Length may not exceed 128 characters")
    private String connectorUri;

    @NotNull
    private boolean enabled;

    @NotEmpty
    @Length(max = 128, message = "Length may not exceed 128 characters")
    private String primaryContactName;

    @Email
    @NotEmpty
    @Length(max = 128, message = "Length may not exceed 128 characters")
    private String primaryContactEmail;

    @Pattern(regexp = "\\d{10}")
    private String primaryContactPhone;


    public Long getOperatorId() {
        return operatorId;
    }

    public void setOperatorId(Long operatorId) {
        this.operatorId = operatorId;
    }

    public String getOperatorName() {
        return operatorName;
    }

    public void setOperatorName(String operatorName) {
        this.operatorName = operatorName;
    }

    public String getApiUri() {
        return apiUri;
    }

    public void setApiUri(String apiUri) {
        this.apiUri = apiUri;
    }

    public String getConnectorUri() {
        return connectorUri;
    }

    public void setConnectorUri(String connectorUri) {
        this.connectorUri = connectorUri;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public String getPrimaryContactName() {
        return primaryContactName;
    }

    public void setPrimaryContactName(String primaryContactName) {
        this.primaryContactName = primaryContactName;
    }

    public String getPrimaryContactEmail() {
        return primaryContactEmail;
    }

    public void setPrimaryContactEmail(String primaryContactEmail) {
        this.primaryContactEmail = primaryContactEmail;
    }

    public String getPrimaryContactPhone() {
        return primaryContactPhone;
    }

    public void setPrimaryContactPhone(String primaryContactPhone) {
        this.primaryContactPhone = primaryContactPhone;
    }
}
