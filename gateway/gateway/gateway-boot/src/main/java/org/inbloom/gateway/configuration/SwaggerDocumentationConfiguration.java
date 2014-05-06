package org.inbloom.gateway.configuration;

import com.mangofactory.swagger.EndpointComparator;
import com.mangofactory.swagger.configuration.DocumentationConfig;
import org.springframework.beans.factory.config.PropertyPlaceholderConfigurer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.core.io.ClassPathResource;

/**
 * Created by lloydengebretsen on 3/7/14.
 */
@Configuration
@ComponentScan("com.mangofactory.swagger.configuration")
public class SwaggerDocumentationConfiguration {

    @Bean
    public PropertyPlaceholderConfigurer swaggerProperties() {
        final PropertyPlaceholderConfigurer swaggerProperties = new PropertyPlaceholderConfigurer();
        swaggerProperties.setLocation(new ClassPathResource("swagger.properties"));
        return swaggerProperties;
    }

}
