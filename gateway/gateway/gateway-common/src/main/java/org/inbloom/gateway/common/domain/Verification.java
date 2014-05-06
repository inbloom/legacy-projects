package org.inbloom.gateway.common.domain;

import java.util.Date;

/**
 * Created by lloydengebretsen on 3/21/14.
 */
public class Verification {

    private Long verificationId;
    private Long userId;
    private Boolean verified = Boolean.FALSE;
    private Date validFrom;
    private Date validUntil;
    private String clientIpAddress;
    private String token;
    private User user;

    public Long getVerificationId() {
        return verificationId;
    }

    public void setVerificationId(Long verificationId) {
        this.verificationId = verificationId;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public Boolean isVerified() {
        return verified;
    }

    public void setVerified(Boolean verified) {
        this.verified = verified;
    }

    public Date getValidFrom() {
        return validFrom;
    }

    public void setValidFrom(Date validFrom) {
        this.validFrom = validFrom;
    }

    public Date getValidUntil() {
        return validUntil;
    }

    public void setValidUntil(Date validUntil) {
        this.validUntil = validUntil;
    }

    public String getClientIpAddress() {
        return clientIpAddress;
    }

    public void setClientIpAddress(String clientIpAddress) {
        this.clientIpAddress = clientIpAddress;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public void activate(Integer timeout) {
        Date now = new Date();
        Date until = new Date(now.getTime() + timeout);
        setValidFrom(now);
        setValidUntil(until);
    }

    public boolean isExpired() {
        return new Date().after(validUntil);
    }

    public Credentials createCredentials(String password) {
        return new Credentials(getUser().getFirstName(), getUser().getLastName(), getUser().getEmail(), password);
    }

    public void validate() {
        setVerified(true);
    }

}
