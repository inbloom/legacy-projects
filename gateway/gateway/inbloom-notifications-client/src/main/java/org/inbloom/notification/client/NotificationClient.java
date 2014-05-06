package org.inbloom.notification.client;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;

/**
 * Singleton entrypoint for sending notifications.  This is a simple implementation.  A more robust impl could force notification services (email, etc) to
 * implement a common interface.
 * TODO Right now we don't have many messages to send so this is an ok, first implementation.  Services could become more course grained by utilizing a notification type enum which has a relationship to a notification type parameters enum (would strongly type a notification to the data it needs to replace tokens for.
 * Created by tfritz on 3/27/14.
 */
public class NotificationClient {

    /** Private constructor prevents instantiation from other classes. */
    private NotificationClient() { }

    /**
     * SingletonHolder is loaded on the first execution of Singleton.getInstance()
     * or the first access to SingletonHolder.INSTANCE, not before.
     */
    private static class SingletonHolder {
        private static  NotificationServiceFacade INSTANCE;
        static {
            synchronized(NotificationClient.class) {
                AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
                NotificationServiceFacade notificationServiceFacade = (NotificationServiceFacade) ctx.getBean("notificationServiceFacade");
                INSTANCE = notificationServiceFacade;
            }
        }
    }

    public static NotificationServiceFacade getInstance() {
        return SingletonHolder.INSTANCE;
    }

}
