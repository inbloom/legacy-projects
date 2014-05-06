package org.inbloom.portal.forms;

import org.inbloom.gateway.common.domain.ApplicationProvider;
import org.inbloom.gateway.common.domain.User;
import org.springframework.web.client.RestTemplate;

/**
 * @author verlinhenderson
 * Date: 4/8/14
 */

public class Registration {
	String firstname;
	String lastname;
	String company;
	String email;

	public void doRegister(String apiHost) {
		User user = new User();
		ApplicationProvider applicationProvider = new ApplicationProvider();
		
		user.setFirstName(firstname);
		user.setLastName(lastname);
		user.setEmail(email);
		applicationProvider.setUser(user);
		applicationProvider.setApplicationProviderName(company);
		
		RestTemplate rt = new RestTemplate();
		rt.postForLocation(apiHost + "/gateway/api/applicationProviders", applicationProvider);
	}
	
	public String getFirstname() {
		return firstname;
	}
	
	public void setFirstname(String firstname) {
		this.firstname = firstname;
	}
	
	public String getLastname() {
		return lastname;
	}

	public void setLastname(String lastname) {
		this.lastname = lastname;
	}
	
	public String getCompany() {
		return company;
	}
	
	public void setCompany(String company) {
		this.company = company;
	}
	
	public String getEmail() {
		return email;
	}
	
	public void setEmail(String email) {
		this.email = email;
	}

}