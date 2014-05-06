package org.inbloom.notification.client.email.messages;

import org.inbloom.notification.client.NotificationException;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.util.StringUtils;

import javax.mail.MessagingException;
import javax.mail.internet.AddressException;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import java.util.ArrayList;
import java.util.List;


/**
 * Encapsulates construction of mime messages using a step builder pattern.
 * Created by tfritz on 3/24/14.
 */
public class MimeMessageBuilder {
    final JavaMailSender mailSender;
    final String charset;
    private String from;
    private final List<String> to = new ArrayList<String>();
    private final List<String> cc = new ArrayList<String>();
    private final List<String> bcc  = new ArrayList<String>();
    private String subject;
    private String body;
    private String replyTo;
    private boolean isHtml = true;

    public MimeMessageBuilder(final JavaMailSender mailSender, final String charset) throws NotificationException {
        if (mailSender == null) {
            throw new NotificationException("An JavaMailSender instance must be provided to the MimeMessageBuilder constructor.");
        }
        if (StringUtils.isEmpty(charset)) {
            throw new NotificationException("An charset value must be provided to the MimeMessageBuilder constructor.");
        }
        this.mailSender = mailSender;
        this.charset = charset;
    }

    public MimeMessageBuilder from(final String from) {
        this.from = from;
        return this;
    }

    public MimeMessageBuilder to(final String to) {
        this.to.add(to);
        return this;
    }

    public MimeMessageBuilder to(final List<String> to) {
        this.to.addAll(to);
        return this;
    }

    public MimeMessageBuilder cc(final String cc) {
        this.cc.add(cc);
        return this;
    }

    public MimeMessageBuilder cc(final List<String> cc) {
        this.cc.addAll(cc);
        return this;
    }

    public MimeMessageBuilder bcc(final String bcc) {
        this.bcc.add(bcc);
        return this;
    }

    public MimeMessageBuilder bcc(final List<String> bcc) {
        this.bcc.addAll(bcc);
        return this;
    }

    public MimeMessageBuilder subject(final String subject) {
        this.subject = subject;
        return this;
    }

    public MimeMessageBuilder body(final String body) {
        this.body = body;
        return this;
    }

    public MimeMessageBuilder replyTo(final String replyTo) {
        this.replyTo = replyTo;
        return this;
    }

    public MimeMessageBuilder isHtml(final boolean isHtml) {
        this.isHtml = isHtml;
        return this;
    }

    /**
     * Performs validation of parameters required by builder.
     */
    protected void validate() throws NotificationException {
        if (StringUtils.isEmpty(subject)) {
            throw new NotificationException("Invalid Mime Message:  a value is required for subject.");
        }
        if (to == null || to.size() == 0) {
            throw new NotificationException("Invalid Mime Message:  at least one To recipient is required.");
        }
        if (StringUtils.isEmpty(from)) {
            throw new NotificationException("Invalid Mime Message:  from is required.");
        }
        if (StringUtils.isEmpty(replyTo)) {
            throw new NotificationException("Invalid Mime Message:  a replyTo is required.");
        }
        if (StringUtils.isEmpty(body)) {
            throw new NotificationException("Invalid Mime Message:  message text is required.");
        }
    }

    /**
     * Builds the MimeMessage from provided values.
     * @return
     * @throws NotificationException
     */
    public MimeMessage build() throws NotificationException {
        /* Perform validations on params supplied to builder before attempting to construct mime message. */
        validate();

        final MimeMessage mimeMessage = mailSender.createMimeMessage();
        final MimeMessageHelper msg = new MimeMessageHelper(mimeMessage, charset);

        try {
            msg.setSubject(subject);
            msg.setFrom(createInternetAddress(from));
            msg.setReplyTo(createInternetAddress(replyTo));

            for (String recipient : to) {
                msg.addTo(createInternetAddress(recipient));
            }

            if (cc != null && cc.size() > 0) {
                for (String recipient : cc) {
                    msg.addCc(createInternetAddress(recipient));
                }
            }

            if (bcc != null && bcc.size() > 0) {
                for (String recipient : bcc) {
                    msg.addBcc(createInternetAddress(recipient));
                }
            }

            msg.setText(body, isHtml);
        } catch (MessagingException me) {
            throw new NotificationException(me);
        }

        return mimeMessage;
    }

    public InternetAddress createInternetAddress(final String address) throws AddressException {
        return new InternetAddress(address);
    }

}
