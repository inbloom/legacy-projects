package org.inbloom.gateway.fixture;

import org.inbloom.gateway.common.domain.ApplicationProvider;
import org.inbloom.gateway.common.status.GatewayStatus;
import org.inbloom.gateway.common.status.Status;
import org.inbloom.gateway.core.event.GatewayAction;
import org.inbloom.gateway.core.event.GatewayRequest;
import org.inbloom.gateway.core.event.GatewayResponse;

/**
 * Created by lloydengebretsen on 3/24/14.
 */
public class ApplicationProviderEventFixtures {

    /**register**/
    public static GatewayRequest<ApplicationProvider> buildRegisterAppProviderEvent() {
        return new GatewayRequest<ApplicationProvider>(GatewayAction.CREATE, ApplicationProviderFixture.buildAppProvider1(null));
    }

    /**modify**/
    public static GatewayRequest<ApplicationProvider> buildModifyAppProviderEvent(Long id) {
        return new GatewayRequest<ApplicationProvider>(GatewayAction.MODIFY, ApplicationProviderFixture.buildAppProvider2(id));
    }

    /**retrieve**/
    public static GatewayRequest<ApplicationProvider> buildRetrieveAppProviderEvent(Long id) {
        ApplicationProvider applicationProvider = new ApplicationProvider();
        applicationProvider.setApplicationProviderId(id);
        return new GatewayRequest<ApplicationProvider>(GatewayAction.RETRIEVE, applicationProvider);
    }

    /**registered**/
    public static GatewayResponse<ApplicationProvider> buildSuccessRegisteredAppProviderEvent(Long id){
        return new GatewayResponse<ApplicationProvider>(GatewayAction.CREATE, ApplicationProviderFixture.buildAppProvider1(id), Status.SUCCESS);
    }

    public static GatewayResponse<ApplicationProvider> buildFailRegisteredAppProviderEvent() {
        return new GatewayResponse<ApplicationProvider>(GatewayAction.CREATE, null, Status.ERROR, "fail");
    }

    /**modified**/
    public static GatewayResponse<ApplicationProvider> buildSuccessModifiedAppProviderEvent(Long id) {
        return new GatewayResponse<ApplicationProvider>(GatewayAction.MODIFY, ApplicationProviderFixture.buildAppProvider2(id), Status.SUCCESS);
    }

    public static GatewayResponse<ApplicationProvider> buildNotFoundModifiedApplicationProviderEvent() {
        return new GatewayResponse<ApplicationProvider>(GatewayAction.MODIFY, null, Status.NOT_FOUND);
    }

    /**retrieved**/
    public static GatewayResponse<ApplicationProvider> buildSuccessRetrievedAppProviderEvent(Long id) {
        return new GatewayResponse<ApplicationProvider>(GatewayAction.RETRIEVE, ApplicationProviderFixture.buildAppProvider2(id), Status.SUCCESS);
    }

    public static GatewayResponse<ApplicationProvider> buildNotFoundRetrievedAppProviderEvent() {
        return new GatewayResponse<ApplicationProvider>(GatewayAction.RETRIEVE, null, Status.NOT_FOUND);
    }


}
