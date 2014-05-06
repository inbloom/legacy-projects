package org.inbloom.notification.client;

/**
 * Created by tfritz on 3/27/14.
 */
public class NotificationException extends Exception {
    public NotificationException(final String msg) {
        super(msg);
    }
    public NotificationException(final Exception e) {
        super(e);
    }
}
