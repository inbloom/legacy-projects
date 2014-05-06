package org.inbloom.portal.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.servlet.http.HttpServletRequest;

/**
 * @author benjaminmorgan
 *         Date: 4/8/14
 */
@Controller
@RequestMapping("/login")
public class LoginController {

    private final Environment env;

    @Autowired
    public LoginController(Environment environment) {
        this.env = environment;
    }

    public String getApiHost() {
        return env.getProperty("apiHost", "http://localhost:9001");
    }

    @RequestMapping(method= RequestMethod.GET)
    public String get(HttpServletRequest request, Model model, RedirectAttributes redirectAttributes) {

        return "login";
    }


    @RequestMapping(method=RequestMethod.POST)
    public String post(Model model, RedirectAttributes redirectAttributes) {

        //TODO: actually log in

        model.addAttribute("errorMessage", "Login functionality has not yet been implemented :P");
        return "login";

    }

}
