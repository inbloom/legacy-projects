package org.inbloom.notification.client;

import org.inbloom.notification.client.email.services.EmailService;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Locale;

/**
 * Created by tfritz on 3/27/14.
 */
public class NotificationServiceFacade {

    @Autowired
    private EmailService emailService;

    /**
     * Builds and sends and account registration confirmation  message, using the specified Locale.
     * @param notificationTypeEnum The type of notification.
     * @param recipientName The name of the recipient the message is intended for.
     * @param recipientEmail The email address to send the message to.
     * @param confirmationLink The link to embed within the email.
     * @param locale The locale for the message (determines which resource bundle is used for multilingual support). Use Locale.ENGLISH.
     * @throws NotificationException
     */
    public void sendAccountRegistrationConfirmation(final NotificationTypeEnum notificationTypeEnum, final String recipientName,
                                                    final String recipientEmail, final String confirmationLink, Locale locale) throws NotificationException {
        if (notificationTypeEnum == null) {
            throw new IllegalStateException("A Notification Type must be provided.");
        }

        switch (notificationTypeEnum) {
            case EMAIL:  this.emailService.sendAccountRegistrationConfirmation(recipientName, recipientEmail,confirmationLink,locale);
                break;
            default:  this.emailService.sendAccountRegistrationConfirmation(recipientName, recipientEmail,confirmationLink,locale);
                break;
        }

    }
}
