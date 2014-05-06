package org.inbloom.notification.domain;

/**
 * Created by tfritz on 3/24/14.
 */
public enum NotificationTemplateEnum {

    CONFIRM_ACCOUNT_REGISTRATION("email-confirm-account-registration.html")
    ;

    private String templateName;

    private NotificationTemplateEnum(final String templateName) {
        this.templateName = templateName;
    }

    public String getTemplateNameName() {
        return templateName;
    }

}
