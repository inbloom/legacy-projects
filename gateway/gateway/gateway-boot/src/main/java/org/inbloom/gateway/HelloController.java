package org.inbloom.gateway;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class HelloController {

    @RequestMapping(value="/", method=RequestMethod.GET)
    public String index() {
        System.out.println("Stuff is happening here!");
        return "index";
    }
}