package org.inbloom.notification.client.email;

import org.inbloom.notification.client.NotificationClient;
import org.inbloom.notification.client.NotificationTypeEnum;
import org.junit.Assert;
import org.junit.Test;
import org.jvnet.mock_javamail.Mailbox;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.mail.Message;
import java.util.List;
import java.util.Locale;

/**
 * Created by tfritz on 3/27/14.
 */
public class TestNotificationClient {
    final Logger log = LoggerFactory.getLogger(TestNotificationClient.class);   //IOC friendly to use instance variable for logger.

    @Test
    public void testNotificationClient() {
        NotificationTypeEnum notificationType = NotificationTypeEnum.EMAIL;
        final String recipientName = "Nasty Ass";
        final String recipientEmail = "nasty.ass@nycsubway.org";
        final String confirmationLink = "http://dummy.com?token=12345";
        final Locale locale = Locale.ENGLISH;

        try {
            Mailbox.clearAll();
            NotificationClient.getInstance().sendAccountRegistrationConfirmation(notificationType, recipientName, recipientEmail, confirmationLink, locale);
            List<Message> inbox = Mailbox.get(recipientEmail);
            log.info("   # of messages within mailbox: " + inbox.size());
            for (Message msg : inbox) {
                log.info("   Content Type: " + msg.getContentType());
                log.info("   Content     : " + (String)msg.getContent());
            }
            //validate the user received the email
            Assert.assertEquals(1, inbox.size());
        } catch (Exception e) {
            log.error(e.getMessage(), e);
        }
        log.info("<<<TestEmailService.testEmailServiceEnglish()");
    }
}
