package org.inbloom.gateway.core.service;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

/**
 * Created By: paullawler
 */
@RunWith(MockitoJUnitRunner.class)
public class TenantServiceTest {

    private SandboxTenantService tenantService;

    @Before
    public void setUp() {
        tenantService = new SandboxTenantService();
    }

    @Test
    public void shouldProvisionALandingZone() {
        tenantService.provisionLandingZone();
    }

}


