package org.inbloom.notification.client;

import org.inbloom.notification.client.email.services.EmailService;
import org.inbloom.notification.client.email.spring.NoticationClientPropertyPlaceholderConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.*;
import org.springframework.context.support.ResourceBundleMessageSource;
import org.springframework.mail.javamail.JavaMailSenderImpl;
import org.thymeleaf.spring4.SpringTemplateEngine;
import org.thymeleaf.templateresolver.ClassLoaderTemplateResolver;

import java.util.Properties;

/**
 * Created by tfritz on 3/26/14.
 */
@Configuration
@Import(NoticationClientPropertyPlaceholderConfig.class)
@ComponentScan(basePackages = {"com.inbloom.notification.client"})
public class AppConfig {

    @Value("${mail.server.host}")
    private String mailServerHost;

    @Value("${mail.server.port}")
    private int mailServerPort;

    @Value("${mail.server.protocol}")
    private String mailServerProtocol;

    @Value("${mail.server.username}")
    private String mailServerUsername;

    @Value("${mail.server.password}")
    private String mailServerPassword;

    /** Javamail property. */
    @Value("${mail.smtp.auth}")
    private String mailSmtpAuth;

    /** Javamail property. */
    @Value("${mail.smtp.starttls.enable}")
    private String mailSmtpStarttlsEnable;

    /** Javamail property. */
    @Value("${mail.smtp.quitwait}")
    private String mailSmtpQuitwait;

    @Value("${saveEmailToFile:false}")
    boolean saveEmailToFile;

    @Bean
    public ResourceBundleMessageSource messageSource() {
        ResourceBundleMessageSource resourceBundleMessageSource = new ResourceBundleMessageSource();
        resourceBundleMessageSource.setBasename("Messages");
        return resourceBundleMessageSource;
    }

    @Bean
    public JavaMailSenderImpl mailSender() {
        JavaMailSenderImpl sender = new JavaMailSenderImpl();
        sender.setHost(this.mailServerHost);
        sender.setPort(this.mailServerPort);
        sender.setProtocol(this.mailServerProtocol);
        sender.setUsername(this.mailServerUsername);
        sender.setPassword(this.mailServerPassword);

        Properties props = new Properties();
        props.put("mail.smtp.auth", this.mailSmtpAuth);
        props.put("mail.smtp.starttls.enable", this.mailSmtpStarttlsEnable);
        props.put("mail.smtp.quitwait", this.mailSmtpQuitwait);
        sender.setJavaMailProperties(props);

        return sender;
    }

    /**
     * THYMELEAF: Template Resolver for email templates
     */
    @Bean
    @Scope ("singleton")
    public ClassLoaderTemplateResolver emailTemplateResolver() {
        ClassLoaderTemplateResolver templateResolver = new ClassLoaderTemplateResolver();
        templateResolver.setPrefix("email-templates/");
        templateResolver.setTemplateMode("HTML5");
        templateResolver.setCharacterEncoding("UTF-8");
        templateResolver.setOrder(Integer.parseInt("1"));
        return templateResolver;
    }

    /**
     * THYMELEAF: Template Engine (Spring4-specific version)
     */
    @Bean
    @Scope ("singleton")
    public SpringTemplateEngine templateEngine() {
        SpringTemplateEngine templateEngine = new SpringTemplateEngine();
        templateEngine.setTemplateResolver(emailTemplateResolver());
        return templateEngine;
    }

    @Bean
    public EmailService emailService() {
        EmailService service = new EmailService();
        service.setSaveEmailToFile(saveEmailToFile);
        return service;
    }

    @Bean
    @Scope ("singleton")
    public NotificationServiceFacade notificationServiceFacade() {
        return new NotificationServiceFacade();
    }
}
