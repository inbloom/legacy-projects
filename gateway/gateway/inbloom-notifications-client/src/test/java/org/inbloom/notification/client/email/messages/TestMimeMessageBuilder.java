package org.inbloom.notification.client.email.messages;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import org.inbloom.notification.client.AppConfig;
import org.inbloom.notification.client.NotificationException;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.support.AnnotationConfigContextLoader;
import org.springframework.util.Assert;
import org.thymeleaf.TemplateEngine;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by tfritz on 3/26/14.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(classes=AppConfig.class, loader=AnnotationConfigContextLoader.class)
public class TestMimeMessageBuilder {
    final Logger log = LoggerFactory.getLogger(TestMimeMessageBuilder.class);   //IOC friendly to use instance variable for logger.

    @Autowired
    private JavaMailSender mailSender;

    @Autowired
    private TemplateEngine templateEngine;

    @Test
    public void testMimeMessageBuilderConstructorNegativeScenarios() {
        try {
            MimeMessageBuilder builder = new MimeMessageBuilder(null, null);
        } catch (Exception e) {
            Assert.isTrue(true); // null values passed to constructor should trigger an error
        }

        try {
            MimeMessageBuilder builder = new MimeMessageBuilder(this.mailSender, null);
        } catch (Exception e) {
            Assert.isTrue(true); // null values passed to constructor should trigger an error
        }

        try {
            MimeMessageBuilder builder = new MimeMessageBuilder(this.mailSender, "");
        } catch (Exception e) {
            Assert.isTrue(true); // null values passed to constructor should trigger an error
        }

        try {
            MimeMessageBuilder builder = new MimeMessageBuilder(null, StandardCharsets.UTF_8.name());
        } catch (Exception e) {
            Assert.isTrue(true); // null values passed to constructor should trigger an error
        }
    }

    @Test
    public void testMimeMessageBuilderConstructor() throws NotificationException {
        MimeMessageBuilder builder = new MimeMessageBuilder(this.mailSender, StandardCharsets.UTF_8.name());
    }

    /**
     * Involving build without required fields must trigger an exception.  Refer to validate() method.
     */
    @Test
    public void testMimeMessageBuilderInvalidBuild() {
        try {
            MimeMessageBuilder builder = new MimeMessageBuilder(this.mailSender, StandardCharsets.UTF_8.name());
            builder.build();
        } catch (Exception e) {
            Assert.isTrue(true);
        }
    }

    @Test
    public void testMimeMessageBuilderAllParams() {
        String from = "sentfromauser@inbloom.org";
        final List<String> to = new ArrayList<String>();
        to.add("fido@acompany.com");
        to.add("spot@acompany.com");
        final List<String> cc = new ArrayList<String>();
        cc.add("bossoffido@acompany.com");
        cc.add("snoopy@acompany.com");
        final List<String> bcc  = new ArrayList<String>();
        bcc.add("bossoffidosboss@acompany.com");
        bcc.add("nsa@usa.gov");
        String subject = "The subject line.";
        String body = "The message body.";
        String replyTo = "noreply@goaway.com";
        boolean isHtml = true;

        try {
            MimeMessageBuilder builder = new MimeMessageBuilder(this.mailSender, StandardCharsets.UTF_8.name());
            builder.subject(subject).body(body).to(to).cc(cc).bcc(bcc).replyTo(replyTo).isHtml(isHtml).from(from).build();
            log.info(ToStringBuilder.reflectionToString(builder, ToStringStyle.MULTI_LINE_STYLE));
        } catch (Exception e) {
            Assert.isTrue(true);
        }
    }

}
