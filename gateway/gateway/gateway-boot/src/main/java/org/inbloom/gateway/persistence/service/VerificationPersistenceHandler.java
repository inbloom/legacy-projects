package org.inbloom.gateway.persistence.service;

import org.inbloom.gateway.common.domain.AccountValidation;
import org.inbloom.gateway.common.domain.User;
import org.inbloom.gateway.common.domain.Verification;
import org.inbloom.gateway.common.status.GatewayStatus;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.persistence.domain.VerificationEntity;
import org.inbloom.gateway.persistence.repository.UserRepository;
import org.inbloom.gateway.persistence.repository.VerificationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.convert.ConversionService;
import org.springframework.stereotype.Service;

import java.util.Date;

/**
 * Created by lloydengebretsen on 3/21/14.
 */
@Service
public class VerificationPersistenceHandler implements VerificationPersistenceService {

    @Autowired
    private VerificationRepository verificationRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ConversionService conversionService;

    @Override
    public GatewayResponse<Verification> createVerification(GatewayRequest<Verification> createVerificationEvent) {

        User user = createVerificationEvent.getPayload().getUser();
        if(user == null){
            //could not find the user so return not found error
            return new GatewayResponse<Verification>(GatewayAction.CREATE, null, Status.NOT_FOUND);
        }

        VerificationEntity verificationEntity = conversionService.convert(createVerificationEvent.getPayload(), VerificationEntity.class);
        verificationEntity.setUserId(user.getUserId());
        verificationEntity.setCreatedAt(new Date());
        verificationRepository.save(verificationEntity);
        return new GatewayResponse<Verification>(GatewayAction.CREATE, conversionService.convert(verificationEntity, Verification.class), Status.SUCCESS);
    }

    @Override
    public GatewayResponse<Verification> retrieveForAccountValidation(GatewayRequest<AccountValidation> validateAccountSetupEvent) {
        VerificationEntity verificationEntity = verificationRepository.findByToken(validateAccountSetupEvent.getPayload().getValidationToken());
        if (verificationEntity == null) {
            return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, null, Status.NOT_FOUND);
        }

        Verification verification = conversionService.convert(verificationEntity, Verification.class);
        User user = conversionService.convert(userRepository.findOne(verification.getUserId()), User.class);
        verification.setUser(user); // todo: CODE REVIEW!!

        return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, verification, Status.SUCCESS);
    }

    @Override
    public GatewayResponse<Verification> modifyVerification(GatewayRequest<Verification> modifyVerificationEvent) {
        VerificationEntity verificationEntity = verificationRepository.findByToken(modifyVerificationEvent.getPayload().getToken());
        if(verificationEntity == null){
            return new GatewayResponse<Verification>(GatewayAction.MODIFY, null, Status.NOT_FOUND);
        }

        verificationEntity.setClientIpAddress(modifyVerificationEvent.getPayload().getClientIpAddress());
        verificationEntity.setVerified(modifyVerificationEvent.getPayload().isVerified());
        verificationEntity.setUpdatedAt(new Date());

        verificationRepository.save(verificationEntity);

        return new GatewayResponse<Verification>(GatewayAction.MODIFY, conversionService.convert(verificationEntity, Verification.class), Status.SUCCESS);
    }

    @Override
    public GatewayResponse<Verification> retrieveVerification(GatewayRequest<Verification> retrieveVerificationEvent) {
        VerificationEntity verificationEntity = verificationRepository.findByToken(retrieveVerificationEvent.getPayload().getToken());
        if (verificationEntity == null)
            return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, null, new GatewayStatus(Status.NOT_FOUND));

        return new GatewayResponse<Verification>(GatewayAction.RETRIEVE, conversionService.convert(verificationEntity, Verification.class), Status.SUCCESS);
    }
}
