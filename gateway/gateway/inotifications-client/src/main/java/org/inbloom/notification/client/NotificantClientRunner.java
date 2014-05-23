package org.inbloom.notification.client;

import org.apache.commons.lang3.exception.ExceptionUtils;

import java.util.Locale;

/**
 * Created by tfritz on 3/27/14.
 */
public class NotificantClientRunner {
    static public void main(String args[]) {
        NotificationTypeEnum notificationType = NotificationTypeEnum.EMAIL;
        final String recipientName = "Nasty Ass";
        final String recipientEmail = "nasty.ass@nycsubway.org";
        final String confirmationLink = "http://dummy.com?token=12345";
        final Locale locale = Locale.ENGLISH;

        try {
            NotificationClient.getInstance().sendAccountRegistrationConfirmation(notificationType, recipientName, recipientEmail, confirmationLink, locale);
        } catch (Exception e) {
            System.out.println(ExceptionUtils.getMessage(e));
        }
    }

}
