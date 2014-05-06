package org.inbloom.portal.util;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.client.ClientHttpResponse;
import org.springframework.web.client.ResponseErrorHandler;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;

/**
 * @author benjaminmorgan
 *         Date: 4/10/14
 */
public class RestTemplateUtil {

    /**
     * Returns a rest template that will ignore HTTP error codes.
     * Instead of throwing an exception, we just return a response ojbect
     * @return RestTemplate
     */
    public static RestTemplate noErrorHandlers()
    {
        RestTemplate rest = new RestTemplate();

        rest.setErrorHandler(new ResponseErrorHandler() {
            @Override
            public boolean hasError(ClientHttpResponse clientHttpResponse) throws IOException {
                return false;
            }

            @Override
            public void handleError(ClientHttpResponse clientHttpResponse) throws IOException {
            }
        });

        return rest;
    }

    /**
     * This object mapper will ignore additional fields that come back in the JSON response
     * that are not in the object
     * @return ObjectMapper for JSON -> Java
     */
    public static ObjectMapper ignoreMissingFieldsMapper() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        return mapper;
    }
}
