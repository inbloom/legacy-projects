package org.inbloom.gateway.persistence.service;

import org.apache.commons.lang.StringUtils;
import org.inbloom.gateway.common.domain.ApplicationProvider;
import org.inbloom.gateway.common.domain.User;
import org.inbloom.gateway.common.status.GatewayStatus;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;
import org.inbloom.gateway.persistence.domain.ApplicationProviderEntity;
import org.inbloom.gateway.persistence.domain.BaseEntity;
import org.inbloom.gateway.persistence.domain.UserEntity;
import org.inbloom.gateway.persistence.repository.ApplicationProviderRepository;
import org.inbloom.gateway.persistence.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.convert.ConversionService;
import org.springframework.stereotype.Service;

import java.util.Date;

/**
 * Created by lloydengebretsen on 3/24/14.
 */
@Service
public class ApplicationProviderPersistenceHandler implements ApplicationProviderPersistenceService {

    @Autowired
    private ApplicationProviderRepository applicationProviderRepository;
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ConversionService conversionService;

    @Override
    public GatewayResponse<ApplicationProvider> createApplicationProvider(GatewayRequest<ApplicationProvider> registerApplicationProviderEvent) {
        ApplicationProviderEntity appProviderEntity = conversionService.convert(registerApplicationProviderEvent.getPayload(), ApplicationProviderEntity.class);
        setCreateData(appProviderEntity);
        applicationProviderRepository.save(appProviderEntity);

        UserEntity userEntity = conversionService.convert(registerApplicationProviderEvent.getPayload().getUser(), UserEntity.class);
        userEntity.setApplicationProviderId(appProviderEntity.getApplicationProviderId());
        setCreateData(userEntity);
        userRepository.save(userEntity);

        ApplicationProvider appProviderDomain = conversionService.convert(appProviderEntity, ApplicationProvider.class);
        appProviderDomain.setUser(conversionService.convert(userEntity, User.class));
        return new GatewayResponse<ApplicationProvider>(GatewayAction.CREATE, appProviderDomain, Status.SUCCESS);
    }

    @Override
    public GatewayResponse<ApplicationProvider> modifyApplicationProvider(GatewayRequest<ApplicationProvider> modifyApplicationProviderEvent) {
        ApplicationProviderEntity retrieved = applicationProviderRepository.findOne(modifyApplicationProviderEvent.getPayload().getApplicationProviderId());
        if(retrieved == null){
            return new GatewayResponse<ApplicationProvider>(GatewayAction.MODIFY, null, Status.NOT_FOUND);
        }

        retrieved.setApplicationProviderName(modifyApplicationProviderEvent.getPayload().getApplicationProviderName());
        retrieved.setOrganizationName(modifyApplicationProviderEvent.getPayload().getOrganizationName());
        setUpdateData(retrieved);
        applicationProviderRepository.save(retrieved);

        ApplicationProvider result = conversionService.convert(retrieved, ApplicationProvider.class);

        UserEntity retrievedUser = userRepository.findByApplicationProviderId(retrieved.getApplicationProviderId());
        setUpdateData(retrievedUser);
        if(StringUtils.isNotBlank(modifyApplicationProviderEvent.getPayload().getUser().getEmail())){
            retrievedUser.setEmail(modifyApplicationProviderEvent.getPayload().getUser().getEmail());
        }
        if(StringUtils.isNotBlank(modifyApplicationProviderEvent.getPayload().getUser().getFirstName())){
            retrievedUser.setFirstName(modifyApplicationProviderEvent.getPayload().getUser().getFirstName());
        }
        if(StringUtils.isNotBlank(modifyApplicationProviderEvent.getPayload().getUser().getLastName())){
            retrievedUser.setLastName(modifyApplicationProviderEvent.getPayload().getUser().getLastName());
        }
        userRepository.save(retrievedUser);
        result.setUser(conversionService.convert(retrievedUser, User.class));

        return new GatewayResponse<ApplicationProvider>(GatewayAction.MODIFY, result,Status.SUCCESS);
    }

    @Override
    public GatewayResponse<ApplicationProvider> retrieveApplicationProvider(GatewayRequest<ApplicationProvider> retrieveApplicationProviderEvent) {
        ApplicationProviderEntity retrieved = applicationProviderRepository.findOne(retrieveApplicationProviderEvent.getPayload().getApplicationProviderId());
        if(retrieved == null) {
            return new GatewayResponse<ApplicationProvider>(GatewayAction.RETRIEVE, null, Status.NOT_FOUND);
        }
        else {
            UserEntity retrievedUser = userRepository.findByApplicationProviderId(retrieved.getApplicationProviderId());
            ApplicationProvider appProviderDomain = conversionService.convert(retrieved, ApplicationProvider.class);
            appProviderDomain.setUser(conversionService.convert(retrievedUser, User.class));
            return new GatewayResponse<ApplicationProvider>(GatewayAction.RETRIEVE, appProviderDomain, Status.SUCCESS);
        }
    }

    public UserEntity getUserByEmail(String email)
    {
        return userRepository.findByEmail(email);
    }

    private void setCreateData(BaseEntity entity){
        entity.setCreatedAt(new Date());
        entity.setCreatedBy("System"); //TODO replace with actual user info after security model is implemented
    }

    private void setUpdateData(BaseEntity entity){
        entity.setUpdatedAt(new Date());
        entity.setUpdatedBy("System"); //TODO replace with actual user info after security model is implemented
    }
}
