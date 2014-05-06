package org.inbloom.notification.client.email.services;

import org.inbloom.notification.client.AppConfig;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.jvnet.mock_javamail.Mailbox;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.support.AnnotationConfigContextLoader;

import javax.mail.Message;
import java.util.List;
import java.util.Locale;

/**
 * Created by tfritz on 3/25/14.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(classes=AppConfig.class, loader=AnnotationConfigContextLoader.class)
public class TestEmailService {
    final Logger log = LoggerFactory.getLogger(TestEmailService.class);   //IOC friendly to use instance variable for logger.

    @Autowired
    private EmailService emailService;

    @Test
    public void testEmailServiceEnglish() {
        log.info(">>>TestEmailService.testEmailServiceEnglish()");
        final String recipientName = "Nasty Ass";
        final String recipientEmail = "nasty.ass@nycsubway.org";
        final String confirmationLink = "http://dummy.com?token=12345";
        final Locale locale = Locale.ENGLISH;

        try {
            Mailbox.clearAll();
            emailService.sendAccountRegistrationConfirmation(recipientName, recipientEmail, confirmationLink, locale);
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

    @Test
    public void testEmailServiceFrench() {
        log.info(">>>TestEmailService.testEmailServiceFrench()");
        final String recipientName = "Nasty Ass";
        final String recipientEmail = "nasty.ass@nycsubway.org";
        final String confirmationLink = "http://dummy.com?token=12345";
        final Locale locale = Locale.FRENCH;

        try {
            Mailbox.clearAll();
            emailService.sendAccountRegistrationConfirmation(recipientName, recipientEmail, confirmationLink, locale);
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
        log.info("<<<TestEmailService.testEmailServiceFrench()");
    }

}

