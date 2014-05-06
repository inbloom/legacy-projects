package org.inbloom.gateway.fixture;

import org.inbloom.gateway.common.domain.User;

/**
 * Created by lloydengebretsen on 3/24/14.
 */
public class UserFixture {

    public static User buildUser(){
        User user = new User();
        user.setEmail("bestappprovider@inbloom.org");
        user.setFirstName("Best");
        user.setLastName("App-Provider");
        return user;
    }

    public static User buildUser(Long id){
        User user = buildUser();
        user.setUserId(id);
        return user;
    }
}
