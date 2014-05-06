package org.inbloom.portal.web;

import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

/**
 * @author benjaminmorgan
 *         Date: 4/15/14
 */
public class ErrorController {

      @RequestMapping(method= RequestMethod.GET)
    public String get(Model model, RedirectAttributes redirectAttributes) {

          return "/error";
    }
}
