package org.inbloom.gateway.fixture;

import org.inbloom.gateway.common.domain.AccountValidation;
import org.inbloom.gateway.common.domain.User;
import org.inbloom.gateway.common.domain.Verification;
import org.joda.time.DateTime;

import java.util.Date;

/**
 * Created By: paullawler
 */
public class VerificationFixture {

    public static Verification expiredVerification(Date validationDate) {
        DateTime validFromDate = new DateTime(validationDate).minusDays(5);
        DateTime validUntilDate = validFromDate.plus(3);

        Verification expired = new Verification();
        expired.setVerificationId(123456L);
        expired.setValidFrom(validFromDate.toDate());
        expired.setValidUntil(validUntilDate.toDate());
        expired.setUser(UserFixture.buildUser());

        return expired;
    }

    public static Verification validVerification(Date validationDate) {
        DateTime validFromDate = new DateTime(validationDate);
        DateTime validUntilDate = validFromDate.plusDays(3);

        Verification valid = new Verification();
        valid.setVerificationId(123456L);
        valid.setValidFrom(validationDate);
        valid.setValidUntil(validUntilDate.toDate());
        valid.setUser(UserFixture.buildUser());

        return valid;
    }

    public static Verification buildUnverifiedVerification(Long userId, Long verificationId)
    {
        Verification verification = new Verification();

        Date now = new Date();
        Date later = new Date(now.getTime() + 4*24*60*60*1000); //4 days later

        User user = UserFixture.buildUser();
        user.setUserId(userId);

        verification.setVerificationId(verificationId);
        verification.setValidFrom(now);
        verification.setValidUntil(later);
        verification.setUser(user);
        verification.setToken("XXSecretRandomTokenXX");
        verification.setVerified(false);

        return verification;
    }

    public static Verification buildVerifiedVerification(Long userId, Long verificationId)
    {
        Verification verification = buildUnverifiedVerification(userId, verificationId);
        verification.setVerified(true);
        verification.setClientIpAddress("192.168.1.1");
        return verification;
    }

    public static AccountValidation accountValidation() {
        return new AccountValidation("sdf090923940290u92", "P@5Sw0rd");
    }

}
